"""Schedulability test implementation and partitioning algorithm comparisons."""

import math

class Task(object):
    """
    Create a class for each task to set up and calculate different parameters of the task.
    """
    def __init__(self, criticality, period, deadline, hi_exec_time, lo_exec_time):
        if deadline is None:
            # implicit deadline by default
            deadline = period
        self.criticality = criticality
        self.period = period
        self.deadline = deadline
        self.hi_exec_time  = hi_exec_time
        self.lo_exec_time = lo_exec_time
        if (criticality == "HI"):
            self.utility = hi_exec_time / period
        else:
            self.utility = lo_exec_time / period
            
def select_partitioning_heuristics():
    """
    Select the four most successful heuristics to be compared in this study.

    Algorithm 1: Racing for heuristics
    Parameters: nRounds, nTests, exploration

    Algorithm 2: Direct heuristic elimination
    Parameters: nRuns, stability

    Output: four best partitioning heuristics
    """

def generate_taskset():
    """
    Generate task utilizations for experiment. Available task generation algorithms are UUniFast
    and the new algorithm proposed by Rodriguez et. al.

    Parameters: UHI(τ), ULO(τ), the ratio of HI tasks (ratioHI = n ), the maximum and minimum
    period nHI (tMax and tMin)
    Output: a set of utilization values
    """
    print("generate_taskset() -- yet to be implemented.")

def assign_priority(tasks):
    """
    Sort the tasks in a taskset using deadline monotonic priority assignment. Shorter deadline
    corresponds to higher priority, and longer deadline corresponds to lower priority.

    Parameters: a random taskset of 1000 tasks
    Output: sorted taskset
    """
    print("assign_priority() -- yet to be implemented.")

def implement_AMC_rtb(tasks, verbose = False):
    """
    Use AMC_rtb as the schedulability test to evaluate the feasibility of an allocation
    before assigning any task to a processor.

    Parameters: taskset partitioned to a processor
    Output: a boolean value of whether or not the allocation is successful
    """
    # create a list of r_lo values to be used in calculating r_star
    r_lo_values = []
    # check schedulability for each task under low mode
    for i in range(len(tasks)):
        # calculate r_lo values
        r_lo = tasks[i].lo_exec_time
        prev_r_lo = 0
        if (verbose == True):
            print("task index =", i + 1)
        while (prev_r_lo != r_lo):
            prev_r_lo = r_lo
            r_lo = tasks[i].lo_exec_time
        # generate the set of all tasks with priority higher than that of t_i, hp_i
        # for each task t_j in hp_i:
            for j in range(i):
                r_lo += math.ceil(prev_r_lo / tasks[j].period) * tasks[j].lo_exec_time
            if (r_lo > tasks[i].deadline):
                return False
            
        # store r_lo values for future use
        r_lo_values.append(r_lo)
        if (verbose == True):
            print("r_lo value = ", r_lo)

    # check schedulability for each HI-criticality task during mode transition
    for i in range(len(tasks)):
        # only make the calculation for HI-criticality tasks
        if (tasks[i].criticality == "HI"):
            # calculate r_star (response time during criticality change) values
            r_star = tasks[i].hi_exec_time
            prev_r_star = 0
            if (verbose == True):
                print("task index =", i + 1)
            while (prev_r_star != r_star):
                prev_r_star = r_star
                r_star = tasks[i].hi_exec_time
                for j in range(i):
                    # accumulate a HI-criticality task
                    if (tasks[j].criticality == "HI"):
                        r_star += math.ceil(prev_r_star / tasks[j].period) * tasks[j].hi_exec_time
                    # accumulate a LO-criticality task
                    else:
                        r_star += math.ceil(r_lo_values[i] / tasks[j].period) * tasks[j].lo_exec_time
                    if (r_star > tasks[i].deadline):
                        return False
            if (verbose == True):
                print("r_star value = ", r_star)
                        
    # check schedulability for each HI-criticality task under high mode
    for i in range(len(tasks)):
        # only make the calculation for HI-criticality tasks
        if (tasks[i].criticality == "HI"):
            # calculate r_lo values
            r_hi = tasks[i].hi_exec_time
            prev_r_hi = 0
            if (verbose == True):
                print("task index =", i + 1)
            # generate the set of all HI-criticality tasks with priority higher than that of t_i, hph_i
            # for each task t_j in hph_i:
            while (prev_r_hi != r_hi):
                prev_r_hi = r_hi
                r_hi = tasks[i].hi_exec_time
                for j in range(i):
                    # accumulate a HI-criticality task
                    if (tasks[j].criticality == "HI"):
                        r_hi += math.ceil(prev_r_hi / tasks[j].period) * tasks[j].hi_exec_time
                    if (r_hi > tasks[i].deadline):
                        return False
            if (verbose == True):
                print("r_hi value = ", r_hi)
    
    # none of the response times pass the deadline
    return True
    
def partition_task_set_method_1():
    """
    Partition the task set with method 1.

    Parameters: tasks, criticalities, utilization values
    Output: tasks on each processor
    """

def implement_first_fit(tasks, n, verbose = False):
    """
    Partition the task set with first fit.

    Parameters: a list of sorted tasks, number of processors
    Output: a list of lists of tasks that are scheduled to each processor
    """
    # create a list of empty lists for generating output
    partitioned_tasks = []
    # create a dictionary that maps the current sum of utilities on each processor to the processor index
    current_total_utilities = {}
    # for testing purpose
    if (verbose == True):
        task_numbers = []
    for i in range(n):
        partitioned_tasks.append([])
        if (verbose == True):
            task_numbers.append([])
        current_total_utilities[i] = 0
    
    # loop through each task
    for i in range(len(tasks)):
        # create a boolean to determine if a task has been partitioned
        partitioned = False
        j = -1
        while (partitioned == False):
            j += 1
            # fail to partition a task
            if (j == n):
                return None
            # check if a task fits on a processor
            if (current_total_utilities[j] + tasks[i].utility <= 1):
                partitioned = True
                current_total_utilities[j] += tasks[i].utility
                partitioned_tasks[j].append(tasks[i])
                if (verbose == True):
                    task_numbers[j].append(i + 1)

    if (verbose == True):
        return task_numbers
    return partitioned_tasks       

def partition_task_set_method_2():
    """
    Partition the task set with method 2.

    Parameters: tasks, criticalities, utilization values
    Output: tasks on each processor
    """

def implement_worst_fit(tasks, n, verbose = False):
    """
    Partition the task set with worst fit.

    Parameters: a list of sorted tasks, number of processors
    Output: a list of lists of tasks that are scheduled to each processor
    """
    # create a list of empty lists for generating output
    partitioned_tasks = []
    # create a dictionary that maps the current sum of utilities on each processor to the processor index
    current_total_utilities = {}
    # for testing purpose
    if (verbose == True):
        task_numbers = []
    for i in range(n):
        partitioned_tasks.append([])
        if (verbose == True):
            task_numbers.append([])
        current_total_utilities[i] = 0
        
    # loop through each task
    for i in range(len(tasks)):
        # initiate the maximum unused capacity and assigned processor index
        max_capacity = 0
        assigned_processor = -1
        for j in range(n):
            if (1 - current_total_utilities[j] > max_capacity and current_total_utilities[j] + tasks[i].utility <= 1):
                max_capacity = 1 - current_total_utilities[j]
                assigned_processor = j
        # fail to partition a task
        if (assigned_processor == -1):
            return None
        partitioned_tasks[assigned_processor].append(tasks[i])
        if (verbose == True):
            task_numbers[assigned_processor].append(i + 1)
        current_total_utilities[assigned_processor] += tasks[i].utility

    if (verbose == True):
        return task_numbers
    return partitioned_tasks

def test_multiprocessor_schedulability(partitioned_tasks, n, verbose = False):
    """
    Return the boolean of whether task set passes/fails with each tested method.

    Parameters: a list of lists of tasks that are scheduled to each processor, number of processors
    Output: whether task set passes/fails with each tested method
    """
    # for each core:
    for i in range(n):
        # if a task cannot be allocated to any processor, the taskset fails automatically
        if (partitioned_tasks is None):
            if (verbose == True):
                print("Failed to allocate a task.")
            return False
        # check schedulability with AMC-rtb: implement_AMC_rtb()
        # if any fails, it is not schedulable
        if (implement_AMC_rtb(partitioned_tasks[i]) == False):
            if (verbose == True):
                print("Schedulability failed on processor", i + 1, ".")
            return False
    # record if task set passes/fails with each tested method
    return True

def conduct_acceptance_ratio_experiment(verbose = False):
    """
    Calculate the acceptance ratio for all tasks as the fraction of tasksets deemed 
    to be schedulable versus total normalized utilization.

    Parameters: a list of normalized utilization values
    Output: acceptance ratio for each utilization
    """
    NUM_OF_PROCESSORS = 3
    NUM_OF_UTILIZATIONS = 20
    ITERATION = 1000
    NUM_OF_METHODS = 2
    if (verbose == True):
        NUM_OF_UTILIZATIONS = 1
        ITERATION = 1
    # create an empty list to store acceptance ratios
    acceptance_ratios = []
    for i in range(NUM_OF_METHODS):
        acceptance_ratios.append([])
    # for each utilization value:
    for i in range(NUM_OF_UTILIZATIONS):
        utilization = i * 0.05
        passing_cases = []
        for j in range(NUM_OF_METHODS):
            passing_cases.append(0)
            
        for j in range(ITERATION):
            # generate a taskset of 80 tasks: generate_taskset()
            current_taskset = generate_taskset()
            # sort the taskset by priority with deadline monotonic priority assignment: assign_priority()
            sorted_tasks = assign_priority(current_taskset)
            if (verbose == True):
                # test with example taskset
                sorted_tasks = [Task("HI", 8, None, 4, 2), Task("LO", 20, None, 9, 3),
                 Task("LO", 35, None, 7, 4), Task("HI", 49, None, 12, 10),
                 Task("LO", 70, None, 14, 11), Task("HI", 17, None, 6, 3),
                 Task("LO", 56, None, 20, 17), Task("HI", 63, None, 15, 12)]
            # partition the taskset with method 1: partition_task_set_method_1()
            first_fit_output = implement_first_fit(sorted_tasks, NUM_OF_PROCESSORS)
            # partition the taskset with method 2: partition_task_set_method_2()
            worst_fit_output = implement_worst_fit(sorted_tasks, NUM_OF_PROCESSORS)
            if (test_multiprocessor_schedulability(first_fit_output, NUM_OF_PROCESSORS) == True):
                # accumulate passing cases
                passing_cases[0] += 1
            else:
                if (verbose == True):
                    test_multiprocessor_schedulability(first_fit_output, NUM_OF_PROCESSORS, True)
            if (test_multiprocessor_schedulability(worst_fit_output, NUM_OF_PROCESSORS) == True):
                # accumulate passing cases
                passing_cases[1] += 1
            else:
                if (verbose == True):
                    test_multiprocessor_schedulability(worst_fit_output, NUM_OF_PROCESSORS, True)
        # calculate passing fraction for each method and store them in the output list
        for j in range(NUM_OF_METHODS):
            acceptance_ratios[j].append(passing_cases[j] / ITERATION)
    # return acceptance ratios list
    return acceptance_ratios

def calculate_weighted_schedulability():
    """
    Another way of comparing heuristic effectiveness.
    """

def make_plots():
    """
    Acceptance_ratio and/or weighted schedulability versus several factors, with
    all four partitioning heuristics in the same figure.
    """
    print(conduct_acceptance_ratio_experiment(True))
    print("make_plots() -- yet to be implemented.")

def test_schedulability_example():
    tasks = [Task("HI", 8, None, 4, 2), Task("LO", 20, None, 9, 3),
             Task("LO", 35, None, 7, 4), Task("HI", 49, None, 12, 10)]
    print(implement_AMC_rtb(tasks, True))

def test_partitioning_example():
    tasks = [Task("HI", 8, None, 4, 2), Task("LO", 20, None, 9, 3),
             Task("LO", 35, None, 7, 4), Task("HI", 49, None, 12, 10),
             Task("LO", 70, None, 14, 11), Task("HI", 17, None, 6, 3),
             Task("LO", 56, None, 20, 17), Task("HI", 63, None, 15, 12)]
    print("First Fit:", implement_first_fit(tasks, 3, True))
    print("Worst Fit:", implement_worst_fit(tasks, 3, True))
