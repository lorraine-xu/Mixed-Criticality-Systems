"""Schedulability test implementation and partitioning algorithm comparisons."""

class Task(object):
    """
    Create a class for each task to set up and calculate different parameters of the task.
    """
    def __init__(self, priority, criticality, period, deadline, low_mode_exec_time, high_mode_exec_time):
        if deadline is None:
            # implicit deadline by default
            deadline = period
        self.priority = priority
        self.criticality = criticality
        self.deadline = deadline
        self.low_mode_exec_time  = low_mode_exec_time
        self.high_mode_exec_time = high_mode_exec_time

    # build more functions on calculating utilization, density, etc.

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

def implement_AMC_rtb():
    """
    Use AMC_rtb as the schedulability test to evaluate the feasibility of an allocation
    before assigning any task to a processor.

    Parameters: task set partitioned to a processor
    Output: a boolean value of whether or not the allocation is successful
    """
    # for each task t_i in the task set:
        # response time during criticality change (r_i_star) = high_mode_exec_time of t_i
        # generate the set of HI-critical tasks with priority higher than or equal to t_i, hph_i
        # for each HI-critical task t_j in hph_i:
            # r_i_star += ceiling(r_i_star / period of t_j) * high_mode_exec_time of t_j
        # generate the set of LO-critical tasks with priority higher than or equal to t_i, hpl_i
        # if the set is nonempty:
            # r_i_lo = low_mode_exec_time of t_i
            # generate the set of all tasks with priority higher than that of t_i, hp_i
            # for each task t_j in hp_i:
                # r_i_lo += ceiling(r_i_lo / period of t_j) * low_mode_exec_time of t_j
            # solve for r_i_lo
        # for each LO-critical task t_k in hpl_i:
            # r_i_star += ceiling(r_i_lo / period of t_k) * low_mode_exec_time of t_k
        # solve for r_i_star
        # if r_i_star > deadline of t_i:
            # return false (unschedulable on the processor)
    # return true

def partition_task_set_method_1():
    """
    Partition the task set with method 1.

    Parameters: tasks, criticalities, utilization values
    Output: tasks on each processor
    """

def partition_task_set_method_2():
    """
    Partition the task set with method 2.

    Parameters: tasks, criticalities, utilization values
    Output: tasks on each processor
    """

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
            ## start with an example task set
            t1 = Task(1, "HI", 8, NONE, 4, 2)
            t2 = Task(2, "LO", 20, NONE, 9, 3)
            t3 = Task(3, "LO", 35, NONE, 7, 4)
            t4 = Task(4, "HI", 49, NONE, 12, 10)
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
