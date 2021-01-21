import joblib
import heapq

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

clf_copy = joblib.load('model.pkl')
x_mean=6.0880456891317545 # <-----------* Set this to the x_mean of the dataset used in training.
sigma=27.867838178747714 # <-----------* Set this to the sigma of the dataset used in training.

def predict(test_example):
    normalized_data = [(x - x_mean) / sigma for x in test_example]

    y_pred = clf_copy.predict([normalized_data])[0]
    y_prob = clf_copy.predict_proba([normalized_data])[0]

    max_probability = "{:.2f}".format(max(y_prob) * 100)
    prediction = int(y_pred)

    predictions = heapq.nlargest(11, range(len(y_prob)), key=y_prob.__getitem__) * 100
    probabilities = heapq.nlargest(11, y_prob) * 100

    return predictions, probabilities