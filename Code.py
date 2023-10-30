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

def generate_task_set():
    """
    Generate task utilizations for experiment. Available task generation algorithms are UUniFast
    and the new algorithm proposed by Rodriguez et. al.

    Parameters: UHI(τ), ULO(τ), the ratio of HI tasks (ratioHI = n ), the maximum and minimum
    period nHI (tMax and tMin)
    Output: a set of utilization values
    """

def implement_AMC_rtb(tasks, verbose = False):
    """
    Use AMC_rtb as the schedulability test to evaluate the feasibility of an allocation
    before assigning any task to a processor.

    Parameters: task set partitioned to a processor
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

def implement_first_fit(tasks, n):
    """
    Partition the task set with first fit.

    Parameters: a list of sorted tasks, number of processors
    Output: a list of lists of tasks that are scheduled to each processor
    """
    # create a list of empty lists for generating output
    partitioned_tasks = []
    # create a dictionary that maps the current sum of utilities on each processor to the processor index
    current_total_utilities = {}
    for i in range(n):
        partitioned_tasks.append([])
        current_total_utilities[i] = 0
    # create a boolean to determine if a task has been partitioned
    partitioned = False
    # loop through each task
    for i in range(len(tasks)):
        j = 0
        while (partitioned == False):
            # check if a task fits on a processor
            if (current_total_utilities[j] + tasks[i].utility <= 1):
                partitioned == True
                current_total_utilities[j] += tasks[i].utility
                partitioned_tasks[j].append(tasks[i])
            j++
            # fail to partition a task
            if (j == n):
                return None
     
    return partitioned_tasks       

def partition_task_set_method_2():
    """
    Partition the task set with method 2.

    Parameters: tasks, criticalities, utilization values
    Output: tasks on each processor
    """

def implement_worst_fit():
    """
    Partition the task set with worst fit.

    Parameters: a list of sorted tasks, number of processors
    Output: a list of lists of tasks that are scheduled to each processor
    """
    # create a list of empty lists for generating output
    partitioned_tasks = []
    # create a dictionary that maps the current sum of utilities on each processor to the processor index
    current_total_utilities = {}
    for i in range(n):
        partitioned_tasks.append([])
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
        current_total_utilities[assigned_processor] += tasks[i].utility
     
    return partitioned_tasks

def conduct_acceptance_ratio_experiment():
    """
    Calculate the acceptance ratio for all tasks as the fraction of task sets deemed 
    to be schedulable versus total normalized utilization.

    Parameters: a list of normalized utilization values
    Output: acceptance ratio for each utilization
    """
    # create an empty list to store acceptance ratios
    # for each utilization value:
        # for i in range(1000):
            # generate a task set of 80 tasks: generate_task_set()
            # sort the task set by priority with deadline monotonic priority assignment: assign_priority()
            # partition the task set with method 1: partition_task_set_method_1()
            # partition the task set with method 2: partition_task_set_method_2()
            # for each core:
                # check schedulability with AMC-rtb: implement_AMC_rtb()
                # if any fails, it is not schedulable
            # record if task set passes/fails with each tested method
        # calculate passing fraction for each method and store them in the output list
    # return acceptance ratio list

def calculate_weighted_schedulability():
    """
    Another way of comparing heuristic effectiveness.
    """

def make_plots():
    """
    Acceptance_ratio and/or weighted schedulability versus several factors, with
    all four partitioning heuristics in the same figure.
    """

def test_example_set():
    tasks = [Task("HI", 8, None, 4, 2), Task("LO", 20, None, 9, 3),
                     Task("LO", 35, None, 7, 4), Task("HI", 49, None, 12, 10)]
    print(implement_AMC_rtb(tasks, True))
