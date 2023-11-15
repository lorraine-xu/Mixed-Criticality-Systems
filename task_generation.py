import numpy
import math

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
      w[i-1, numpy.arange(1,(i+1))] = tmp1 + tmp2;
      tmp3 = w[i-1, numpy.arange(1,(i+1))] + tiny;
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

def quantize_params(taskset):
  """After applying overheads, use this function to make
      task parameters integral again."""

  for t in taskset:
      t.hi_exec_time     = int(math.ceil(t.hi_exec_time))
      t.period   = int(math.floor(t.period))
      t.deadline = int(math.floor(t.deadline))

  return taskset

def gen_mixed_criticality_taskset(period_min, period_max, num_of_tasks, utilization, scale=ms2us):
  from main import Task
  x = StaffordRandFixedSum(num_of_tasks, utilization, 1)
  periods = gen_periods(num_of_tasks, 1, period_min, period_max)
  ts = []

  C = scale(x[0] * periods)

  taskset = numpy.c_[x[0], C[0] / periods[0], periods[0], C[0]]
  for t in range(numpy.size(taskset,0)):
      ts.append(Task("HI", scale(taskset[t][2]), None, taskset[t][3], 0.0003487754111160126))
      print(Task("HI", scale(taskset[t][2]), None, taskset[t][3], 0.0003487754111160126).utilization)

  quantize_params(ts)
  return ts