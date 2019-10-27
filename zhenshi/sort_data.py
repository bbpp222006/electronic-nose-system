import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import signal



def pinghua(data):
    chuangkou = 20
    for i, rs in enumerate(data):
        if i == len(data[:, 0]) - chuangkou:
            break
        data[i, :] = np.mean(data[i:i + chuangkou, :], axis=0)

    return data
