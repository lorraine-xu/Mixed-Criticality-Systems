"""Schedulability test implementation and partitioning algorithm comparisons."""

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

    Parameters: processors, execution time, deadline, criticality, priority
    Output: a boolean value of whether or not the allocation is successful
    """

def partition_all_tasks():
    """
    Follow the algorithm of CA-UDP to complete the partitioning of all tasks.

    Parameters: tasks, criticalities, utilization values
    Output: tasks on each processor
    """

def calculate_acceptance_ratio():
    """
    Calculate the acceptance ratio for all tasks as the fraction of task sets deemed 
    to be schedulable versus total normalized utilization.

    Parameters: normalized utilization, list of tasks
    Output: acceptance ratio
    """

def calculate_weighted_schedulability():
    """
    Another way of comparing heuristic effectiveness.
    """

def make_plots():
    """
    Acceptance_ratio and/or weighted schedulability versus several factors, with
    all four partitioning heuristics in the same figure.
    """