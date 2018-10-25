import pandas as pd 
import numpy as np
import matplotlib.pylab as plt

# from utils import *


def componentMethod(data):
    return


def PTEquivalence(data):  # input dataset, output: ONE dataset with index = TCID and 2 columns latitude, and longitude
    out = data[['LONGITUDE', 'LATITUDE']].set_index('TCID')
    return out


def zTransform(data, bit):  # input: dataset and desired bit, output: ONE dataset where index = TCID, and 1 column, Z

    lon_max = data['LONGITUDE'].max()
    lat_max = data['LATITUDE'].max()

    lon_min = data['LONGITUDE'].min()
    lat_min = data['LATITUDE'].min()

    diff_lon = lon_max - lon_min
    diff_lat = lat_max - lat_min

    if diff_lon > diff_lat:
        diff = diff_lon - diff_lat

        lat_max += diff
    else:
        diff = diff_lat - diff_lon

        lon_max += diff

    diff_lon = lon_max - lon_min
    diff_lat = lat_max - lat_min

    data['Y'] = np.floor(((data['LATITUDE'] - lat_min) / diff_lat) * (2 ** bit))
    data['X'] = np.floor(((data['LONGITUDE'] - lon_min) / diff_lon) * (2 ** bit))

    X = data['X'].values.tolist()
    Y = data['Y'].values.tolist()

    z = []
    for i in range(len(X)):
        val = 0
        for j in range(17):
            val = val | ((int(X[i]) & (2 ** j)) << (j + 1))
            val = val | ((int(Y[i]) & (2 ** j)) << (j))
        z.append(val)

    data['Z'] = z

    out = data[['Z', 'TCID']].set_index('TCID')
    return out


# used to determine the optimal number of bit to be used in the Z-Transform
def bitDetermination(data):  # input dataset, output plot
    lon_max = data['LONGITUDE'].max()
    lat_max = data['LATITUDE'].max()

    lon_min = data['LONGITUDE'].min()
    lat_min = data['LATITUDE'].min()

    diff_lon = lon_max - lon_min
    diff_lat = lat_max - lat_min

    if diff_lon > diff_lat:
        diff = diff_lon - diff_lat

        lat_max += diff
    else:
        diff = diff_lat - diff_lon

        lon_max += diff

    diff_lon = lon_max - lon_min
    diff_lat = lat_max - lat_min

    bit = range(4, 20)

    key_number = []
    for num in bit:
        data['Y'] = np.floor(((data['LATITUDE'] - lat_min) / diff_lat) * (2 ** num))
        data['X'] = np.floor(((data['LONGITUDE'] - lon_min) / diff_lon) * (2 ** num))

        x = data['x'].values.tolist()
        y = data['y'].values.tolist()

        z = []

        # Z-order transformation
        for i in range(len(x)):
            val = 0
            for j in range((num * 2) + 1):
                val = val | ((int(x[i]) & (2 ** j)) << (j + 1))
                val = val | ((int(y[i]) & (2 ** j)) << j)
            z.append(val)

        data['Z'] = z

        print(num, data.Z.nunique())
        key_number.append(data.Z.nunique())

    plt.plot(bit, key_number, 'bx-')
    plt.xlabel('Bit Number')
    plt.ylabel('Number of Unique Z')
    plt.title('NUmber of Unique Z vs Bit Number')
    return
