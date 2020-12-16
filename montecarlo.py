import numpy as np
import multiprocessing
from timeit import default_timer as timer
import time
import sys

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
    
def calculate_var_worker(count, samples):
    # Disable catching KeyboardInterrupt in the worker processes.
    # Main process will catch it instead and terminate workers.
    if sys.platform == "win32":
        import win32api
        win32api.SetConsoleCtrlHandler(None, True)
        
    area_vec = []
    for i in range(count):
        area_vec.append(calculate_area(samples))
    variance = np.var(area_vec)
    return variance

def calculate_var(count, samples):
    cores = int(multiprocessing.cpu_count() - 1)
    pool = multiprocessing.Pool(cores)
    results = []
    for core in range(cores):
        results.append(pool.apply_async(calculate_var_worker,
                                         (int(count/cores), samples, )))

    variances = []
    for result in results:
        while(1):
            try:
                variances.append(result.get(1))
                break
            except multiprocessing.context.TimeoutError:
                pass
            except KeyboardInterrupt: # Ctrl C has been clicked
                print("terminating program")
                pool.terminate()
                pool.close()
                pool.join()
                raise KeyboardInterrupt
    pool.close()
    pool.join()
    return np.mean(variances)

