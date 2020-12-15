import numpy as np
#from timeit import default_timer as timer
#import time

np.random.seed()

class FunctionGivenLUT:
    def __init__(self, lut_path, lut_arg_start, lut_step):
        self._step = lut_step
        self._arg_start = lut_arg_start
        self._data =  np.fromfile(lut_path, dtype=np.float64)

    def get(self, xarg):
        lut_index = int((xarg - self._arg_start) / self._step)
        return self._data[lut_index]

def calculate_area(samples):
    lut = FunctionGivenLUT("lut_1e5.bin", -np.pi/2, 1e-5)
    k = 0
    rectangle_area = np.pi * 1
    px = np.random.uniform(low=-np.pi/2, high=np.pi/2, size=samples)
    py = np.random.uniform(low=0, high=1, size=samples)
    f = [lut.get(x) for x in px]
    for i in range(samples):
        if (f[i] >= py[i]):
           k = k+1 # samples hit
    area = rectangle_area*k/samples
    return area

