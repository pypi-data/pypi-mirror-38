"""
schedBebida
~~~~~~~~~

This scheduler is the implementation of the BigData scheduler for the
Bebida on batsim project.

It is a Simple fcfs algoritihm.

It take into account preemption by respounding to Add/Remove resource
events. It kills the jobs that are allocated to removed resources. It also
kill some jobs in the queue in order to re-schedule them on a larger set of
resources.

The Batsim job profile "msg_hg_tot" or a sequence of that kind of jobs are
MANDATORY for this mechanism to work.

Also, the `--dynamic-jobs-enabled` Batsim CLI option MUST be set, while
`--profiles-forwarded-on-submission` and `--dynamic_jobs_acknowledged`
must NOT be set.
"""

from batsim.batsim import BatsimScheduler, Job

from procset import ProcSet, ProcInt
import logging
import copy
import random
import math
from itertools import islice


def sort_by_id(jobs):
    return sorted(jobs, key=lambda j: int(j.id.split('!')[1].split('#')[0]))


def generate_pfs_io_profile(profile_dict, job_alloc, io_alloc, pfs_id):
    # Generating comm matrix
    bytes_to_read = profile_dict["io_reads"] / len(job_alloc)
    bytes_to_write = profile_dict["io_writes"] / len(job_alloc)
    comm_matrix = []
    for col, machine_id_col in enumerate(io_alloc):
        for row, machine_id_row in enumerate(io_alloc):
            if row == col or (
                    pfs_id != machine_id_row and
                    pfs_id != machine_id_col):
                comm_matrix.append(0)
            elif machine_id_row == pfs_id:
                # Reads to pfs
                comm_matrix.append(bytes_to_read)
            elif machine_id_col == pfs_id:
                # Writes to pfs
                comm_matrix.append(bytes_to_write)

    io_profile = {
        "type": "msg_par",
        "cpu": [0] * len(io_alloc),
        "com": comm_matrix
    }
    return io_profile


def nth(iterable, n):
    return next(islice(iterable, n, None))


def fill_storage_map(compute_resources, storage_resources):
    """
    WARNING: The local disk resource name MUST be prefixed by the host
    resource name
    """
    storage_map = {}
    for res_id, compute in compute_resources.items():
        for storage_id, storage in storage_resources.items():
            if compute["name"] in storage["name"]:
                storage_map[res_id] = storage_id
    return storage_map


def index_of(alloc, host_id):
    """ Return the index of the given host id in the given alloc """
    for index, host in enumerate(alloc):
        if host == host_id:
            return index
    raise Exception("Host id not found in the allocation")


def local_disk_in_alloc(host_id, alloc, storage_map):
    """ Return true if the host_id has is local disk in the alloc """
    disk_id = storage_map[host_id]
    return disk_id in alloc


def new_io_profile_name(base_job_profile, io_profiles):
    new_name = base_job_profile + "_io#0"
    counter = 0
    while new_name in io_profiles:
        new_name = new_name.rsplit('#')[0] + '#' + str(counter)
        counter = counter + 1
    return new_name


def generate_dfs_io_profile(
        profile_dict,
        job_alloc,
        io_alloc,
        remote_block_location_list,
        block_size_in_MB,
        locality,
        storage_map,
        replication_factor=3):
    """
    Every element of the remote_block_location_list is a host that detain a block to
    read.
    """
    block_size_in_Bytes = block_size_in_MB * 1024 * 1024
    # Generates blocks read list from block location: Manage the case where
    # dataset input size is different from the IO reads due to partial or
    # multiple reads of the dataset
    nb_blocks_to_read = int(
            math.ceil(profile_dict["io_reads"] / block_size_in_Bytes))

    nb_blocks_to_read_local = math.ceil(nb_blocks_to_read * locality / 100)
    nb_blocks_to_read_remote = nb_blocks_to_read - nb_blocks_to_read_local

    comm_matrix = [0] * len(io_alloc) * len(io_alloc)

    # Fill in reads in the matrix
    host_that_read_index = 0
    for _ in range(nb_blocks_to_read):
        col = host_that_read_index
        host_id = nth(job_alloc, host_that_read_index)

        # Only pick local reads if the host AND its disk is involved
        # in the io_alloc
        if (nb_blocks_to_read_local > 0 and
                local_disk_in_alloc(host_id, io_alloc, storage_map)):

            row = index_of(io_alloc, storage_map[host_id])
            nb_blocks_to_read_local = nb_blocks_to_read_local - 1

        # This is a remote read
        else:
            row = index_of(io_alloc,
                    remote_block_location_list[nb_blocks_to_read_remote %
                        len(remote_block_location_list)])
            nb_blocks_to_read_remote = nb_blocks_to_read_remote - 1

        comm_matrix[(row * len(io_alloc)) + col] += block_size_in_Bytes

        # Round robin trough the hosts
        host_that_read_index = (host_that_read_index + 1) % len(job_alloc)


    # Generates writes block list
    nb_blocks_to_write = int(
            (profile_dict["io_writes"] / block_size_in_Bytes) + 1)

    # Fill in writes in the matrix
    host_that_write_index = 0
    for _ in reversed(range(nb_blocks_to_write)):

        host_id = nth(job_alloc, host_that_write_index)
        # Only use hosts AND its disk is involved in the io_alloc
        while (not local_disk_in_alloc(host_id, io_alloc, storage_map)):
            host_that_write_index = (host_that_write_index + 1) % len(job_alloc)
            host_id = nth(job_alloc, host_that_write_index)

        col = index_of(io_alloc, storage_map[host_id])
        row = host_that_write_index

        # fill the matrix
        comm_matrix[(row * len(io_alloc)) + col] += block_size_in_Bytes

        # manage the replication
        # (local -> racklocal_i) + (racklocal_i -> other_i)^N-2
        for _ in range(replication_factor):
            col = row
            # WARNING: disks for replica writes are randomly pick in io_alloc
            # not on the whole cluster
            # NOTE: We can also manage write location here (under HPC node or
            # not)
            row = random.choice(list(io_alloc))

        # Round robin trough the hosts
        host_that_write_index = (host_that_write_index + 1) % len(job_alloc)

    io_profile = {
        "type": "msg_par",
        "cpu": [0] * len(io_alloc),
        "com": comm_matrix
    }
    return io_profile


class SchedBebida(BatsimScheduler):

    def filter_jobs_by_state(self, state):
        return sort_by_id([job for job in self.bs.jobs.values() if
            job.job_state == state])

    def running_jobs(self):
        return self.filter_jobs_by_state(Job.State.RUNNING)

    def to_schedule_jobs(self):
        if len(self.filter_jobs_by_state(Job.State.IN_SUBMISSON)) > 0:
            return []
        return self.filter_jobs_by_state(Job.State.SUBMITTED)

    def in_killing_jobs(self):
        return self.filter_jobs_by_state(Job.State.IN_KILLING)

    def allocate_first_fit_in_best_effort(self, job):
        """
        return the allocation with as much resources as possible up to
        the job's `requeqted_resources` number.
        return None if no resources at all are available.
        """
        self.logger.info("Try to allocate Job: {}".format(job.id))
        assert job.allocation is None , (
               "Job allocation should be None and not {}".format(job.allocation))

        nb_found_resources = 0
        allocation = ProcSet()
        nb_resources_still_needed = job.requested_resources

        iter_intervals = (self.free_resources & self.available_resources).intervals()
        for curr_interval in iter_intervals:
            if (len(allocation) >= job.requested_resources):
                break
            #import ipdb; ipdb.set_trace()
            interval_size = len(curr_interval)
            self.logger.debug("Interval lookup: {}".format(curr_interval))

            if interval_size > nb_resources_still_needed:
                allocation.insert(
                    ProcInt(
                        inf=curr_interval.inf,
                        sup=(curr_interval.inf + nb_resources_still_needed -1))
                )
            elif interval_size == nb_resources_still_needed:
                allocation.insert(copy.deepcopy(curr_interval))
            elif interval_size < nb_resources_still_needed:
                allocation.insert(copy.deepcopy(curr_interval))
                nb_resources_still_needed = nb_resources_still_needed - interval_size

        if len(allocation) > 0:
            job.allocation = allocation
            job.state = Job.State.RUNNING

            # udate free resources
            self.free_resources = self.free_resources - job.allocation

            self.logger.info("Allocation for job {}: {}".format(
                job.id, job.allocation))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_be_removed_resources = {}
        self.load_balanced_jobs = set()
        # TODO use CLI options
        #self.variant = "pfs"
        if "variant" not in self.options:
            self.variant = "no-io"
        else:
            self.variant = self.options["variant"]

    def onSimulationBegins(self):
        self.free_resources = ProcSet(*[res_id for res_id in
            self.bs.resources.keys()])
        self.nb_total_resources = len(self.free_resources)
        self.available_resources = copy.deepcopy(self.free_resources)

        if self.variant == "pfs":
            assert self.bs.nb_storage_resources == 1, (
                "Exactly one storage node is necessary for the 'pfs' variant")
            # WARN: This implies that at exactlly one storage is defined
            self.pfs_id = [key for key,value in self.bs.storage_resources.items() if
                    "role" in value["properties"] and
                    value["properties"]["role"] == "storage"][0]

        elif self.variant == "dfs":
            self.storage_map = fill_storage_map(self.bs.resources,
                    self.bs.storage_resources)

            # check if all the nodes have a storage attached
            assert all([res in self.storage_map for res in
                self.bs.resources])

            # size of the DFS block
            if "dfs_block_size_in_MB" not in self.options:
                self.block_size_in_MB = 128
            else:
                self.block_size_in_MB = self.options["block_size_in_MB"]
            self.logger.info("Block size in MB for the DFS: {}".format(
                self.block_size_in_MB))

            ## Locality default values are taken from Bebida experiments
            ## observed locality. For more details See:
            ## https://gitlab.inria.fr/mmercier/bebida/blob/master/experiments/run_bebida/bebida_results_analysis.ipynb

            # Level of locality
            if "node_locality_in_percent" not in self.options:
                self.node_locality_in_percent = 70
            else:
                self.node_locality_in_percent = self.options["node_locality_in_percent"]

            # Level of locality variation (uniform)
            if "node_locality_variation_in_percent" not in self.options:
                self.node_locality_variation_in_percent = 10
            else:
                self.node_locality_variation_in_percent = self.options["node_locality_variation_in_percent"]

            self.logger.info("Node locality is set to: {}% +- {}%".format(
                self.node_locality_in_percent,
                self.node_locality_variation_in_percent))

            # Fix the seed to have reproducible DFS behavior
            random.seed(0)

        assert self.bs.batconf["profiles-forwarded-on-submission"] == True, (
                "Forward profile is mandatory for resubmit to work")

    def onJobSubmission(self, job):
        profile_dict = self.bs.profiles[job.workload][job.profile]
        assert "type" in profile_dict, "Forward profile is mandatory"
        assert (profile_dict["type"] == "msg_par_hg_tot" or
                profile_dict["type"] == "composed")

    def onJobCompletion(self, job):
        # If it is a job killed, resources where already where already removed
        # and we don't want other jobs to use these resources.
        # But, some resources of the allocation are not part of the removed
        # resources: we have to make it available
        if job.job_state == Job.State.COMPLETED_KILLED:
            to_add_resources = job.allocation & self.available_resources
            self.logger.debug("To add resources: {}".format(to_add_resources))
            self.free_resources = self.free_resources | to_add_resources
        else:
            # udate free resources
            self.free_resources = self.free_resources | job.allocation
            self.load_balance_jobs()

    def onNoMoreEvents(self):
        if len(self.free_resources) > 0:
            self.schedule()

        self.logger.debug("=====================NO MORE EVENTS======================")
        self.logger.debug("FREE RESOURCES = {}".format(str(self.free_resources)))
        self.logger.debug("AVAILABLE RESOURCES = {}".format(str(self.available_resources)))
        self.logger.debug("TO BE REMOVED RESOURCES: {}".format(str(self.to_be_removed_resources)))
        nb_used_resources = self.nb_total_resources - len(self.free_resources)
        nb_allocated_resources = sum([len(job.allocation) for job in
            self.running_jobs()])
        self.logger.debug(("NB USED RESOURCES = {}").format(nb_used_resources))
        self.logger.debug('NO MORE STATIC JOBS: {}'.format(
            self.bs.no_more_static_jobs))
        self.logger.debug("SUBMITTED JOBS = {}".format(
            self.bs.nb_jobs_submitted))
        self.logger.debug("IN_SUBMISSON JOBS = {}".format(
            self.bs.nb_jobs_in_submission))
        self.logger.debug("SCHEDULED JOBS = {}".format(
            self.bs.nb_jobs_scheduled))
        self.logger.debug("COMPLETED JOBS = {}".format(
            self.bs.nb_jobs_completed))
        self.logger.debug("JOBS: \n{}".format(self.bs.jobs))

        if (self.bs.nb_jobs_scheduled == self.bs.nb_jobs_completed
                and self.bs.no_more_static_jobs
                and self.bs.nb_jobs_in_submission == 0
                and len(self.running_jobs()) == 0
                and len(self.in_killing_jobs()) == 0):
            self.bs.notify_registration_finished()

    def onRemoveResources(self, resources):
        self.available_resources = self.available_resources - ProcSet.from_str(resources)

        # find the list of jobs that are impacted
        # and kill all those jobs
        to_be_killed = []
        for job in self.running_jobs():
            if job.allocation & ProcSet.from_str(resources):
                to_be_killed.append(job)

        if len(to_be_killed) > 0:
            self.bs.kill_jobs(to_be_killed)

        # check that no job in Killing are still allocated to this resources
        # because some jobs can be already in killing before this function call
        self.logger.debug("Jobs that are in killing: {}".format(self.in_killing_jobs()))
        in_killing = self.in_killing_jobs()
        if not in_killing or all([len(job.allocation & ProcSet.from_str(resources)) == 0
                                for job in in_killing]):
            # notify resources removed now
            self.bs.notify_resources_removed(resources)
        else:
            # keep track of resources to be removed that are from killed jobs
            # related to a previous event
            self.to_be_removed_resources[resources] = [
                    job for job in
                    in_killing if len(job.allocation &
                        ProcSet.from_str(resources)) != 0]

    def onAddResources(self, resources):
        to_add_resources = ProcSet.from_str(resources)
        assert len(to_add_resources & ProcSet(*self.bs.storage_resources)) == 0, (
                "Resources to be added should not contain storage resources!")
        self.available_resources = self.available_resources | to_add_resources
        # add the resources
        self.free_resources = self.free_resources | to_add_resources

        self.load_balance_jobs()

    def load_balance_jobs(self):
        """
        find the list of jobs that need more resources
        kill jobs, so tey will be resubmited taking free resources, until
        tere is no more resources
        """
        free_resource_nb = len(self.free_resources)
        to_be_killed = []

        for job in self.running_jobs():
            wanted_resource_nb = job.requested_resources - len(job.allocation)
            if wanted_resource_nb > 0:
                to_be_killed.append(job)
                free_resource_nb = free_resource_nb - wanted_resource_nb
            if free_resource_nb <= 0:
                break
        if len(to_be_killed) > 0:
            self.bs.kill_jobs(to_be_killed)
            # mark those jobs in order to resubmit them without penalty
            self.load_balanced_jobs.update({job.id for job in to_be_killed})

    def onJobsKilled(self, jobs):
        # First notify that the resources are removed
        to_remove = []
        for resources, to_be_killed in self.to_be_removed_resources.items():
            if (len(to_be_killed) > 0
                and any([job in jobs for job in to_be_killed])):
                # Notify that the resources was removed
                self.bs.notify_resources_removed(resources)
                to_remove.append(resources)
                # Mark the resources as not available
                self.free_resources = self.free_resources - ProcSet.from_str(resources)
        # Clean structure
        for resources in to_remove:
            del self.to_be_removed_resources[resources]

        # get killed jobs progress and resubmit what's left of the jobs
        for old_job in jobs:
            progress = old_job.progress
            if "current_task_index" not in progress:
                new_job = old_job
            else:
                # WARNING only work for simple sequence job without sub sequence
                curr_task = progress["current_task_index"]
                # get profile to resubmit current and following sequential
                # tasks
                new_job_seq_size = len(old_job.profile_dict["seq"][curr_task:])
                old_job_seq_size = len(old_job.profile_dict["seq"])

                self.logger.debug("Job {} resubmitted stages: {} out of {}".format(
                        old_job.id,
                        new_job_seq_size,
                        old_job_seq_size))

                if old_job.id in self.load_balanced_jobs:
                    # clean the set
                    self.load_balanced_jobs.remove(old_job.id)

                    # Create a new job with a profile that corespond to the work that left
                    curr_task_progress = progress["current_task"]["progress"]
                    if curr_task_progress == 0 and curr_task == 0:
                        # No need to create a new profile
                        new_job = old_job
                    else:
                        new_job = copy.deepcopy(old_job)
                        new_job.profile = old_job.profile + "#" + str(curr_task) + "#" + str(curr_task_progress)
                        new_job.profile_dict["seq"] = old_job.profile_dict["seq"][curr_task:]

                        # Store the new job profile to be submitted if not
                        # already registerd
                        to_submit = {}
                        if new_job.profile not in self.bs.profiles[new_job.workload]:
                            to_submit = {new_job.profile: new_job.profile_dict}

                        # only recreate a profile if it has started
                        if curr_task_progress != 0:
                            # Now let's modify the current internal profile to reflect progress
                            assert "profile" in progress["current_task"], ('The profile'
                                    ' is not forwarded in the job progress: set'
                                    ' {"job_kill": {"forward_profiles": true}} in the '
                                    'batsim config')
                            curr_task_profile = progress["current_task"]["profile"]
                            assert curr_task_profile["type"] == "msg_par_hg_tot", "Only msg_par_hg_tot profile are supported right now"
                            for key, value in curr_task_profile.items():
                                if isinstance(value, (int, float)):
                                    curr_task_profile[key] = value * (1 - curr_task_progress)
                            parent_task_profile = progress["current_task"]["profile_name"].split("#")[0]
                            curr_task_profile_name =  parent_task_profile + "#" + str(curr_task_progress)

                            new_job.profile_dict["seq"][0] = curr_task_profile_name
                            to_submit[curr_task_profile_name] = curr_task_profile

                        # submit the new internal current task profile
                        self.bs.register_profiles(new_job.workload, to_submit)

                elif (new_job_seq_size == old_job_seq_size):
                    # FIXME does it takes into account current task progress?
                    # no modification to do: resubmit the same job
                    new_job = old_job
                else:
                    # create a new profile: remove already finished stages
                    new_job = copy.deepcopy(old_job)
                    new_job.profile = old_job.profile + "#" + str(curr_task)
                    new_job.profile_dict["seq"] = old_job.profile_dict["seq"][curr_task:]
                    self.bs.register_profiles(new_job.workload,
                            {new_job.profile: new_job.profile_dict})

            # Re-submit the profile
            self.bs.resubmit_job(new_job)

    def onDeadlock(self):
        pass

    def schedule(self):
        # Implement a simple FIFO scheduler
        if len(self.free_resources & self.available_resources) == 0:
            return
        to_execute = []
        to_schedule_jobs = self.to_schedule_jobs()
        self.logger.info("Start scheduling jobs, nb jobs to schedule: {}".format(
            len(to_schedule_jobs)))

        self.logger.debug("jobs to be scheduled: \n{}".format(to_schedule_jobs))

        io_jobs = {}
        for job in to_schedule_jobs:
            if len(self.free_resources & self.available_resources) == 0:
                break

            all_profiles = self.bs.profiles[job.workload]

            self.logger.debug('Scheduling variant: {}'.format(self.variant))
            if self.variant == "no-io":
                # Allocate resources
                self.allocate_first_fit_in_best_effort(job)
                to_execute.append(job)

            # Manage IO
            elif self.variant == "pfs":
                # Allocate resources
                self.allocate_first_fit_in_best_effort(job)
                to_execute.append(job)

                alloc = job.allocation | ProcSet(ProcInt(self.pfs_id, self.pfs_id))

                # Manage Sequence job
                if job.profile_dict["type"] == "composed":
                    io_profiles = {}
                    # Generate profile sequence
                    for profile_name in job.profile_dict["seq"]:
                        profile = all_profiles[profile_name]
                        new_profile_name = new_io_profile_name(profile_name,
                                list(all_profiles.keys()) +
                                list(io_profiles.keys()))
                        io_profiles[new_profile_name] = generate_pfs_io_profile(
                                profile,
                                job.allocation,
                                alloc,
                                self.pfs_id)
                    # submit these profiles
                    assert len(io_profiles) == len(job.profile_dict["seq"])
                    self.bs.register_profiles(job.workload, io_profiles)

                    # Create io job
                    io_job = {
                      "alloc": str(alloc),
                      "profile_name": new_io_profile_name(job.id, all_profiles),
                      "profile": {
                        "type": "composed",
                        "seq": list(io_profiles.keys())
                      }
                    }

                else:
                    io_job = {
                      "alloc": str(alloc),
                      "profile_name": new_io_profile_name(job.id, all_profiles),
                      "profile": generate_pfs_io_profile(job.profile_dict,
                                job.allocation,
                                alloc,
                                self.pfs_id)
                    }

                io_jobs[job.id] = io_job

            elif self.variant == "dfs":
                # Get input size and split by block size
                nb_blocks_to_read = math.ceil((job.profile_dict["input_size_in_GB"] * 1024)  /
                        self.block_size_in_MB)

                # Allocate resources
                self.allocate_first_fit_in_best_effort(job)
                to_execute.append(job)

                # randomly pick some nodes where the blocks are while taking
                # into account locality percentage
                job_locality = self.node_locality_in_percent + random.uniform(
                        - self.node_locality_variation_in_percent,
                        self.node_locality_variation_in_percent)

                nb_blocks_to_read_local = math.ceil(nb_blocks_to_read *
                        job_locality / 100)
                nb_blocks_to_read_remote = nb_blocks_to_read - nb_blocks_to_read_local

                assert nb_blocks_to_read_remote + nb_blocks_to_read_local == nb_blocks_to_read

                remote_block_location_list = [
                        random.choice(list(self.bs.storage_resources.keys())) for _
                        in range(nb_blocks_to_read_remote)]

                io_alloc = job.allocation | ProcSet(*remote_block_location_list)

                # Manage Sequence job
                if job.profile_dict["type"] == "composed":
                    # TODO split IO quantity between stages
                    io_profiles = {}
                    # Generate profile sequence
                    for profile_name in job.profile_dict["seq"]:
                        profile = self.bs.profiles[job.workload][profile_name]
                        io_profile_name = new_io_profile_name(job.id,
                                list(all_profiles.keys()) +
                                list(io_profiles.keys()))
                        self.logger.debug("Creating new profile: " +
                                io_profile_name)
                        io_profiles[io_profile_name] = generate_dfs_io_profile(
                                profile,
                                job.allocation,
                                io_alloc,
                                remote_block_location_list,
                                self.block_size_in_MB,
                                job_locality,
                                self.storage_map)
                    # submit these profiles
                    self.bs.register_profiles(job.workload, io_profiles)

                    # Create io job
                    io_job = {
                      "alloc": str(io_alloc),
                      "profile_name": new_io_profile_name(job.id + "_seq_",
                          self.bs.profiles[job.workload]),
                      "profile": {
                        "type": "composed",
                        "seq": list(io_profiles.keys())
                      }
                    }

                else:
                    io_job = {
                      "alloc": str(alloc),
                      "profile_name": new_io_profile_name(job.id, all_profiles),
                      "profile": generate_dfs_io_profile(
                                job.profile_dict,
                                job.allocation,
                                io_alloc,
                                nb_blocks_to_read_local,
                                remote_block_location_list,
                                self.block_size_in_MB,
                                job_locality,
                                self.bs.resources,
                                self.bs.storage_resources)
                    }

                io_jobs[job.id] = io_job

            else:
                raise Exception("This variant type '{}' does not exists".format(self.variant))

        self.bs.execute_jobs(to_execute, io_jobs)
        for job in to_execute:
            job.job_state = Job.State.RUNNING
        self.logger.info("Finished scheduling jobs, nb jobs scheduled: {}".format(
            len(to_execute)))
        self.logger.debug("jobs to be executed: \n{}".format(to_execute))

