import numpy as np
import pandas as pd
import math
import pdb

def read_data(x_csv, y_csv):
    x_data = pd.read_csv(x_csv, header=None)
    y_data = pd.read_csv(y_csv, header=None)

    x_data = x_data.to_numpy()
    y_data = y_data.to_numpy()
    #x_data = transpose_x_data(x_data) # If needed
    y_data = np.transpose(y_data)[0]
    
    return x_data, y_data

def visual_data_example(nbr: int, x_data, y_data):
    instances = np.where(y_data==nbr)

    samples = np.arange(N_SAMPLES * N_ELECTRODES)
    major_ticks = [N_SAMPLES*i for i in range(N_ELECTRODES + 1)]
    minor_ticks = [N_SAMPLES*i + N_SAMPLES/2 for i in range(N_ELECTRODES)]

    x_plot = x_data[instances[0][0]]

    fig, ax = plt.subplots()
    ax.plot(samples, x_plot)
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.xaxis.set_tick_params(length=10, width=1, which='major')
    ax.xaxis.set_tick_params(length=0, width=0, which='minor')
    ax.set_xticklabels(["", "", "", "", "", "", "", "", "", "", "", ""])
    ax.set_xticklabels(["E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11"], minor=True)
    ax.grid(which='major', axis='x', alpha=0.8)
    plt.xlim([0, 1200])
    plt.ylim([0, 250])
    plt.title(touches[nbr])
    plt.xlabel('areas over time')
    plt.ylabel('touch strength')

    plt.show()

x_data, y_data = read_data('visualized_data_x.csv', 'visualized_data_y.csv')

for i in range(12):
    visual_data_example(i, x_data, y_data)