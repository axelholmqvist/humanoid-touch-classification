import numpy as np
import pandas as pd
import math
import pdb

import joblib

import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from printer import touches

N_SAMPLES = 100
N_ELECTRODES = 12

TEST_SIZE = 0.15
N_EPOCHS = 10


# Some data only contain zeros. This remove them. 
def remove_zero_data(x_data, y_data):
    delete_idx = []
    for idx, x in enumerate(x_data):
        if np.linalg.norm(x) == 0:
            delete_idx.append(idx)
        
    new_x = np.delete(x_data, delete_idx, axis = 0)
    new_y = np.delete(y_data, delete_idx, axis = 0)
    return new_x, new_y


def normalize_data(x_data):
    x_mean = np.mean(x_data)
    sigma = np.std(x_data)
    x_min = np.min(x_data)
    x_max = np.max(x_data)
    x_data = (x_data-x_mean)/sigma # Normal distrubution
    #print(f'x_mean={x_mean}, sigma={sigma}, x_min={x_min}') # <-----------*  Need these values for our predictor.
    return x_data


def train(x_data, y_data):
    print('\n\nTraining stared...\nEpochs: ' + str(N_EPOCHS) + ', Validation size: ' + str(TEST_SIZE))
    clf = svm.SVC(kernel='rbf', C=100, class_weight='balanced', probability=True)
    accuracies = []
    confusion_matrices = []
    for k in range(N_EPOCHS):
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=TEST_SIZE, stratify = y_data)

        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)

        accuracy = metrics.accuracy_score(y_test, y_pred)
        accuracies.append(accuracy)
        c_matrix = confusion_matrix(y_test, y_pred)
        confusion_matrices.append(c_matrix)
    print(f'\n_____________________________________________________________')
    print('Training finished:')
    print("\nAverage prediction accuracy after " + str(N_EPOCHS) +  " validations:", '{:0.2f}'.format(np.mean(accuracies)))
    export_model(clf)
    return accuracies, confusion_matrices


def read_data(x_csv, y_csv):
    x_data = pd.read_csv(x_csv, header=None)
    y_data = pd.read_csv(y_csv, header=None)

    x_data = x_data.to_numpy()
    y_data = y_data.to_numpy()
    #x_data = transpose_x_data(x_data) # If needed
    y_data = np.transpose(y_data)[0]
    
    return x_data, y_data


def transpose_x_data(x_data):
    for i, mat in enumerate(x_data):
        mat = mat.reshape((-1,N_ELECTRODES))
        mat=np.array([np.array(xi) for xi in mat])
        x_data[i] = mat.flatten('F')
    return x_data


def remove_data(nbr, amount, x_data, y_data):
    instances = np.where(y_data==nbr)
    delete_idx = instances[0][0:amount]
    new_x = np.delete(x_data, delete_idx, axis = 0)
    new_y = np.delete(y_data, delete_idx, axis = 0)
    return x_data, y_data


def export_model(clf):
    joblib.dump(clf, 'model.pkl', compress=9)


def run(x_data, y_data):
    accuracies, confusion_matrices = train(x_data, y_data)
    val = np.min(accuracies)
    i = np.argmin(accuracies)
    print("Lowest prediction accuracy: " + '{:0.2f}'.format(val))
    print('\nConfusion matrix of lowest validation round: ')
    print(confusion_matrices[i])
    print(f'_____________________________________________________________')
    print('\n\n')
    return accuracies, confusion_matrices

def main():
    x_data, y_data = read_data('training_data_x.csv', 'training_data_y.csv')
    x_data, y_data = remove_zero_data(x_data, y_data)
    x_data = normalize_data(x_data)
    accuracies, confusion_matrices = run(x_data, y_data)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nTraining aborted.\n')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)












