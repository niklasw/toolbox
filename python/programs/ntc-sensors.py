#!/usr/bin/env python3

import csv
import sys, os, io
from matplotlib import pyplot as plt
from numpy import array, append, transpose

sensor_data='''
"Temperature", "PAW_A2W", "NTC_3k", "NTC_5k", "NTC_10k-2", "NTC-10k-3", "Unknown", "NTC_20k", "NTC_100k"
-40, 167.82, 100.9, 89.49, 336.4, 239.7, 188.4, 814.0, 4095   
-30, 93.05, 53.09, 54.07, 177.0, 135.3, 111.3, 415.6, 2077   
-20, 53.92, 29.12, 33.21, 97.08, 78.91, 67.74, 220.6, 1105   
-10, 32.10, 16.60, 21.07, 55.33, 47.54, 42.45, 122.4, 612.4  
0,  19.70,  9.795, 13.73, 32.65, 29.49, 27.28, 70.20, 351.0  
10, 12.443, 5.969, 9.041, 19.90, 18.79, 17.96, 41.56, 207.8  
20, 8.044 , 3.747, 6.064, 12.49, 12.26, 12.09, 25.34, 126.7  
25, 6.523 , 3.000, 5.000, 10.00, 10.00, 10.00, 20.00, 100.00 
30, 5.326 , 2.417, 4.139, 8.057, 8.194, 8.313, 15.88, 79.43  
40, 3.615 , 1.598, 2.875, 5.327, 5.592, 5.828, 10.21, 51.06  
50, 2.508 , 1.081, 2.032, 3.603, 3.893, 4.161, 6.718, 33.60  
60, 1.777 , 0.746, 1.463, 2.488, 2.760, 3.021, 4.518, 22.59  
70, 1.279 , 0.525, 1.069, 1.751, 1.990, 2.229, 3.100, 15.50  
80, 0.932 , 0.376, 0.792, 1.255, 1.458, 1.669, 2.168, 10.84  
90, 0.686 , 0.275, 0.601, 0.915, 1.084, 1.266, 1.542, 7.707  
100, 0.511, 0.203, 0.464, 0.678, 0.817, 0.973, 1.114, 5.571  
110, 0.390, 0.536, 0.354, 0.512, 0.624, 0.752, 0.818, 4.092  
120, 0.302, 0.123, 0.272, 0.410, 0.481, 0.605, 0.609, 3.046  
130, 0.236, 0.097, 0.212, 0.322, 0.380, 0.487, 0.460, 2.298  
140, 0.186, 0.077, 0.169, 0.257, 0.300, 0.395, 0.351, 1.755  
150, 0.147, 0.063, 0.137, 0.210, 0.240, 0.325, 0.271, 1.356'''


def csv_reader(data):
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            print(row)
            yield row


def read_csv_from_file(filename):
    with open(filename, newline='') as f:
        for row in csv_reader(f):
            yield row


def read_csv_from_string(str_data):
    data = io.StringIO(str_data)
    for row in csv_reader(data):
        if row:
            yield row


def csv_to_array(string_data):
    reader = read_csv_from_string(string_data)
    header = next(reader)
    header = [v.strip('" ') for v in header]
    n_cols = len(header)
    rows = []
    for item in reader:
        try:
            rows += [float(v) for v in item]
        except:
            continue
    n_rows = int(len(rows)/n_cols)
    data = array(rows)
    data.shape = (n_rows, n_cols)
    print(f'Data shape = {data.shape}')
    print(f'headers =')
    for item in header:
        print(f'        {item}')
    data = transpose(data)
    return (header, data)


#         PAW_A2W
#         NTC_3k
#         NTC_5k
#         NTC_10k-2
#         NTC-10k-3
#         Unknown
#         NTC_20k
#         NTC_100k

def run():
    sys.argv.append('aquarea-optional-sensors-characteristics.csv')
    filename = sys.argv[1]
    headers, data = csv_to_array(sensor_data)

    col_selection = 'PAW_A2W NTC_5k NTC_10k-2'.split()

    temperatures = data[0]
    kOhms = data[1:]
    for item in col_selection:
        index = headers[1:].index(item)
        plt.plot(temperatures, kOhms[index], label=item)
    plt.legend()
    plt.grid('on')
    plt.yscale('log')
    plt.show()


if __name__ == '__main__':
    run()



