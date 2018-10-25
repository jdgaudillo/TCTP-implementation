import pandas as pd 
import numpy as np

# from utils import *


def componentMethod(data):
    return


def PTEquivalence(data):  # input dataset, output: ONE dataset with index = TCID and 2 columns latitude, and longitude
    out = data[['LONGITUDE', 'LATITUDE']].set_index('TCID')
    return out


def zTransform(data):  # input: dataset and desired bit, output: ONE dataset where index = TCID, and 1 column, Z

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

    number = range(4, 20)

    value = 0
    for num in number:
        data['Y'] = np.floor(((data['LATITUDE'] - lat_min) / diff_lat) * (2 ** num))
        data['X'] = np.floor(((data['LONGITUDE'] - lon_min) / diff_lon) * (2 ** num))

        x = data['X'].values.tolist()
        y = data['Y'].values.tolist()

        z = []

        # Z-order transformation
        for i in range(len(x)):
            val = 0
            for j in range((num * 2) + 1):
                val = val | ((int(x[i]) & (2 ** j)) << (j + 1))
                val = val | ((int(y[i]) & (2 ** j)) << j)
            z.append(val)

        data['Z'] = z

        if num == 4 or value != data.Z.nunique():
            value = int(data.Z.nunique())
        else:
            break

    bit = num - 1
    data['Y'] = np.floor(((data['LATITUDE'] - lat_min) / diff_lat) * (2 ** bit))
    data['X'] = np.floor(((data['LONGITUDE'] - lon_min) / diff_lon) * (2 ** bit))

    x = data['X'].values.tolist()
    y = data['Y'].values.tolist()

    z = []
    for i in range(len(x)):
        val = 0
        for j in range(17):
            val = val | ((int(x[i]) & (2 ** j)) << (j + 1))
            val = val | ((int(y[i]) & (2 ** j)) << j)
        z.append(val)

    data['Z'] = z

    out = data[['Z', 'TCID']].set_index('TCID')
    return out
