from __future__ import print_function
import re
import math
import os.path
import collections
import sys
import pdb
from string import Template

__VERSION__ = '0.6.20'

##########################################
# Fits line to inlier data using RANSAC
##########################################


def main():
    xs = [10, 20]
    ys = [20, 30]
    n = 10
    fitLine(xs, ys, n)


def fitLine(xs, ys, n, random_seed=None):
    import random
    from scipy import stats
    inlierData = []
    data = []
    # Used for testing, delete before commit
    data.append([20, 30])
    data.append([4, 70])
    data.append([2, 80])
    data.append([20, 8])
    data.append([21, 7])
    data.append([9, 1])
    data.append([2, 1])
    data.append([8, 1])
    data.append([9, 3])
    data.append([9, 2])
    data.append([9, 4])
    data.append([5, 37])
    data.append([2, 47])
    data.append([3, 43])
    data.append([4, 44])
    data.append([13, 45])
    data.append([21, 48])
    data.append([91, 37])
    data.append([94, 23])
    data.append([9, 26])
    data.append([51, 22])
    data.append([23, 44])
    data.append([32, 43])
    data.append([27, 6])
    data.append([10, 7])
    data.append([20, 4])
    data.append([20, 30])
    data.append([4, 70])
    data.append([2, 80])
    data.append([20, 8])
    data.append([21, 7])
    data.append([9, 1])
    data.append([2, 1])
    data.append([8, 1])
    data.append([9, 3])
    data.append([9, 2])
    data.append([9, 4])
    data.append([5, 37])
    data.append([2, 47])
    data.append([3, 43])
    data.append([4, 44])
    data.append([13, 45])
    data.append([21, 48])
    data.append([91, 37])
    data.append([94, 23])
    data.append([9, 26])
    data.append([51, 22])
    data.append([23, 44])
    data.append([32, 43])
    data.append([27, 6])
    data.append([10, 7])
    data.append([20, 4])
    data.append([20, 30])
    data.append([4, 70])
    data.append([2, 80])
    data.append([20, 8])
    data.append([21, 7])
    data.append([9, 1])
    data.append([2, 1])
    data.append([8, 1])
    data.append([9, 3])
    data.append([9, 2])
    data.append([9, 4])
    data.append([5, 37])
    data.append([2, 47])
    data.append([3, 43])
    data.append([4, 44])
    data.append([13, 45])
    data.append([21, 48])
    data.append([91, 37])
    data.append([94, 23])
    data.append([9, 26])
    data.append([51, 22])
    data.append([23, 44])
    data.append([32, 43])
    data.append([27, 6])
    data.append([10, 7])
    data.append([20, 4])

    for a in range(len(xs)):
        data.append([xs[a], ys[a]])
        T = .01  # inlier threshold
        n = 10
        max_iterations = 1000
#     pdb.set_trace()
        # to pass, it needs to use 96% of data in linear regression
        goal_inliers = int(.96 * len(data))
        best_ic = 0
        best_model = None
        random.seed(random_seed)
        data = list(data)  # "random" needs data to be in list form

        for i in range(max_iterations):
            s = random.sample(data, int(n))
            m = _estimate(s)
            ic = 0
            del inlierData[:]
            for j in range(len(data)):
                if _is_inlier(m, data[j], T):
                    inlierData.append(data[j])
                    ic += 1

            print('random sample:', s)
            print('estimate:', m,)
            print('# inliers:', ic)

            if ic > best_ic:
                best_ic = ic
                # best_model = m
                best_model = _estimate(inlierData)
                if ic > goal_inliers:
                    break
                print('took iterations:', i+1, 'best model',
                      best_model, 'explains:', best_ic)
                print('data length:', len(data))
#     pdb.set_trace()
                xs_tmp = map(lambda t: t[0], inlierData)
                ys_tmp = map(lambda t: t[1], inlierData)
                lineregressRANSAC = stats.linregress(xs_tmp, ys_tmp)
#     result = stats.linregress(inlierData)
#     r_value = result.rvalue
#     xs = inlierData.xs
#     ys = inlierData(ys)
                print(inlierData)
                return lineregressRANSAC
        # return float(best_model[2])
        # return r_value


def _augment(xys):
    import numpy as np
    axy = np.ones((len(xys), 3))
    axy[:, :2] = xys
    return axy


def _estimate(xys):
    import numpy as np
    axy = _augment(xys[:2])
    return np.linalg.svd(axy)[-1][-1, :]


def _is_inlier(coeffs, xy, threshold):
    import numpy as np
    # import pdb; pdb.set_trace()
    # print(np.abs(coeffs.dot(_augment([xy]).T)))
    return np.abs(coeffs.dot(_augment([xy]).T)) < threshold
