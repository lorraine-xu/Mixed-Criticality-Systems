def generate_taskset():
  """
  Generate task utilizations for experiment. Available task generation algorithms are UUniFast
  and the new algorithm proposed by Rodriguez et. al.

  Parameters: UHI(τ), ULO(τ), the ratio of HI tasks (ratioHI = n ), the maximum and minimum
  period nHI (tMax and tMin)
  Output: a set of utilization values
  """
  print("generate_taskset() -- yet to be implemented.")

  # Reference:
#   # wrapper for generating task sets for use within the schedcat library
# # parameters:
# #   periods:                one from NAMED_PERIODS (period definitions similar to those used in tasksets.py
# #   period_distribution:    'unif' or 'logunif' for uniform or log-based distribution
# #   tasks_n:                number of tasks to be generated
# #   utilization:            target utilization of the task set to be generated
# def gen_taskset(periods, period_distribution, tasks_n, utilization,
#                 period_granularity=None, scale=ms2us, want_integral=True):
#     if periods in NAMED_PERIODS:
#         # Look up by name.
#         (period_min, period_max) = NAMED_PERIODS[periods]
#     else:
#         # If unknown, then assume caller specified range manually.
#         (period_min, period_max) = periods
#     x = StaffordRandFixedSum(tasks_n, utilization, 1)
#     if period_granularity is None:
#         period_granularity = period_min
#     periods = gen_periods(tasks_n, 1, period_min, period_max, period_granularity, period_distribution)
#     ts = TaskSystem()

#     periods = numpy.maximum(periods[0], max(period_min, period_granularity))

#     C = scale(x[0] * periods)

#
#     taskset = numpy.c_[x[0], C / periods, periods, C]
#     for t in range(numpy.size(taskset,0)):
#         ts.append(SporadicTask(taskset[t][3], scale(taskset[t][2])))

#     if want_integral:
#         quantize_params(ts)
#     return ts

## In our case, system utilization is high utilization

# def gen_periods(n, nsets, min, max, gran, dist):

#     if dist == "logunif":
#         periods = numpy.exp(numpy.random.uniform(low=numpy.log(min), high=numpy.log(max+gran), size=(nsets,n)))
#     elif dist == "unif":
#         periods = numpy.random.uniform(low=min, high=(max+gran), size=(nsets,n))
#     elif type(dist) == list:
#         # Interpret as set of pre-defined periods to choose from.
#         assert nsets == 1
#         # avoid numpy.random.choice() because we need to be compatible with 1.6.X
#         periods = [random.choice(dist) for _ in xrange(n)]
#         # wrap in numpy types
#         periods = numpy.array(periods)
#         periods.shape = (1, n)
#     else:
#         return None

#     periods = numpy.floor(periods / gran) * gran

#     return periods


# def tasks(self, max_tasks=None, max_util=None, squeeze=False,
#               time_conversion=trunc):
#       """Generate a sequence of tasks until either max_tasks is reached
#       or max_util is reached. If max_util would be exceeded and squeeze is
#       true, then the last-generated task's utilization is scaled to exactly
#       match max_util. Otherwise, the last-generated task is discarded.
#       time_conversion is used to convert the generated (non-integral) values
#       into integral task parameters.
#       """
#       count = 0
#       usum  = 0
#       while ((max_tasks is None or count < max_tasks) and
#              (max_util is None  or usum  < max_util)):
#           period   = self.period()
#           util     = self.util()
#           cost     = period * util
#           deadline = self.deadline(cost, period)
#           # scale as required
#           period   = max(1,    int(time_conversion(period)))
#           cost     = max(1,    int(time_conversion(cost)))
#           deadline = max(1, int(time_conversion(deadline)))
#           util = cost / period
#           count  += 1
#           usum   += util
#           if max_util and usum > max_util:
#               if squeeze:
#                   # make last task fit exactly
#                   util -= (usum - max_util)
#                   cost = trunc(period * util)
#               else:
#                   break
#           yield ts.SporadicTask(cost, period, deadline)

## In our case, we also need to assign a criticality level value to a task in the tasks() function,
## based on the ratio of HI tasks.

## Need another function to make HI-LO couples making sure that for each HI task the HI utilization is higher than the LO utilization.
