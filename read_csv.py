import pandas as pd
import numpy as np

## FOR NORMAL DATA SET, TO CONVERT IT
#x_data = pd.read_csv('training_data_x.csv')
#x_data = x_data.to_numpy()

#for i, mat in enumerate(x_data):
#    mat = mat.reshape((-1,12))
#    mat=np.array([np.array(xi) for xi in mat])
#    x_data[i] = mat.flatten('F')

## FOR ALREADY CONVERTED DATA SET
x_data = pd.read_csv('converted_training_data_x.csv')
x_data = x_data.to_numpy()

return x_data