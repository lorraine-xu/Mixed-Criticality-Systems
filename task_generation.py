import numpy
import random as ra

def generate_taskset():
  """
  Generate task utilizations for experiment. Available task generation algorithms are UUniFast
  and the new algorithm proposed by Rodriguez et. al.

  Parameters: UHI(τ), ULO(τ), the ratio of HI tasks (ratioHI = n ), the maximum and minimum
  period nHI (tMax and tMin)
  Output: a set of utilization values
  """
  print("generate_taskset() -- yet to be implemented.")

def ms2us(ms):
    return ms * 1000

def StaffordRandFixedSum(n, u, nsets):

  #deal with n=1 case
  if n == 1:
      return numpy.tile(numpy.array([u]),[nsets,1])

  k = numpy.floor(u)
  s = u
  step = 1 if k < (k-n+1) else -1
  s1 = s - numpy.arange( k, (k-n+1)+step, step )
  step = 1 if (k+n) < (k-n+1) else -1
  s2 = numpy.arange( (k+n), (k+1)+step, step ) - s

  tiny = numpy.finfo(float).tiny
  huge = numpy.finfo(float).max

  w = numpy.zeros((n, n+1))
  w[0,1] = huge
  t = numpy.zeros((n-1,n))

  for i in numpy.arange(2, (n+1)):
      tmp1 = w[i-2, numpy.arange(1,(i+1))] * s1[numpy.arange(0,i)]/float(i)
      tmp2 = w[i-2, numpy.arange(0,i)] * s2[numpy.arange((n-i),n)]/float(i)
      w[i-1, numpy.arange(1,(i+1))] = tmp1 + tmp2
      tmp3 = w[i-1, numpy.arange(1,(i+1))] + tiny
      tmp4 = numpy.array( (s2[numpy.arange((n-i),n)] > s1[numpy.arange(0,i)]) )
      t[i-2, numpy.arange(0,i)] = (tmp2 / tmp3) * tmp4 + (1 - tmp1/tmp3) * (numpy.logical_not(tmp4))

  m = nsets
  x = numpy.zeros((n,m))
  rt = numpy.random.uniform(size=(n-1,m)) #rand simplex type
  rs = numpy.random.uniform(size=(n-1,m)) #rand position in simplex
  s = numpy.repeat(s, m)
  j = numpy.repeat(int(k+1), m)
  sm = numpy.repeat(0, m)
  pr = numpy.repeat(1, m)

  for i in numpy.arange(n-1,0,-1): #iterate through dimensions
      e = ( rt[(n-i)-1,...] <= t[i-1,j-1] ) #decide which direction to move in this dimension (1 or 0)
      sx = rs[(n-i)-1,...] ** (1/float(i)) #next simplex coord
      sm = sm + (1-sx) * pr * s/float(i+1)
      pr = sx * pr
      x[(n-i)-1,...] = sm + pr * e
      s = s - e
      j = j - e #change transition table column if required

  x[n-1,...] = sm + pr * s

  #iterated in fixed dimension order but needs to be randomised
  #permute x row order within each column
  for i in range(0,m):
      x[...,i] = x[numpy.random.permutation(n),i]

  return numpy.transpose(x)

def gen_periods(n, nsets, min, max):
  periods = numpy.exp(numpy.random.uniform(low=numpy.log(min), high=numpy.log(max), size=(nsets,n)))
  return periods

def gen_mixed_criticality_taskset(period_min, period_max, num_of_tasks, hi_utilization, lo_utilization, hi_probability, verbose = False):
  from main import Task
  hi_x = StaffordRandFixedSum(num_of_tasks, hi_utilization, 1)
  lo_x = StaffordRandFixedSum(num_of_tasks, lo_utilization, 1)
  max_hi_utilization = max(hi_x)
  min_hi_utilization = min(hi_x)
  periods = gen_periods(num_of_tasks, 1, period_min, period_max)
  ts = []

  hi_C = hi_x[0] * periods
  lo_C = lo_x[0] * periods

  taskset = numpy.c_[periods[0], hi_C[0], lo_C[0]]
  # print(hi_x)
  # print(periods)
  # print(hi_C)
  criticality_levels = gen_criticality_level(hi_probability, num_of_tasks)
  for t in range(numpy.size(taskset,0)):
      current_task = Task(criticality_levels[t], taskset[t][0], None, taskset[t][1], taskset[t][2])
      # print(criticality_levels[t])
      # print(current_task.hi_utilization)
      # print(current_task.lo_utilization)
      if (current_task.criticality == "HI"):
         new_hi_utilization = current_task.hi_utilization
        #  print(new_hi_utilization)
        #  print(current_task.lo_utilization)
        #  print(new_hi_utilization.size)
         lo_utilization = current_task.lo_utilization
        #  print(lo_utilization.size)
         print("min", min_hi_utilization)
         print("max", max_hi_utilization)
         while (new_hi_utilization < lo_utilization):
            new_hi_utilization = ra.uniform(min_hi_utilization, max_hi_utilization)
            print("random number", new_hi_utilization)
         taskset[t][1] = taskset[t][0] * new_hi_utilization
         current_task = Task(criticality_levels[t], taskset[t][0], None, taskset[t][1], taskset[t][2])
         print("break")
         print(current_task.hi_utilization)
         print(current_task.lo_utilization)
      ts.append(current_task)
      print(current_task.lo_utilization)
      # new_sum += current_task.hi_utilization
  # print(new_sum)
  # sort the taskset by period (deadline monotonic priority assignment)
  ts.sort(key = lambda x: x.period)
  # print("split")
  # for task in ts:
  #    print(task.period)
  if (verbose == True):
     data = []
     for i in range(len(ts)):
        data.append([ts[i].criticality, ts[i].period, ts[i].hi_exec_time, ts[i].lo_exec_time])
     print(data)
  return ts

def gen_criticality_level(hi_probability, num_of_tasks):
  criticality_levels = []
  for i in range(num_of_tasks):
    if ra.random() < hi_probability:
      criticality_levels.append("HI")
    else:
      criticality_levels.append("LO")
  return criticality_levels

def couple_hi_lo(hi_C, lo_C):
   """
   To be implemented.
   """

# print(gen_criticality_level(0.2, 10))