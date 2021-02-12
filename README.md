# Humanoid Touch Classification
*Technical system with applied machine learning (SVM) for a project in MAMN10/MAMN15 @ Lund University.*

Supplementary code for the prototype created in "A system for Bidirectional Touch-Emotion Interaction for a Humanoid Robot" by Axel Holmqvist, Martin Karlsson and Mariam Mirström.

## Short Description
A project has been carried out with the purpose of constructing a somatosensory system for a humanoid robot, including the identification of different types of touch and a related response. The detection of touch on an Epi humanoid robot head is made from conductive paint on the inside on the head shell, the electrical signal produced is processed into a digital representation of touch, a classification of touch is made through the use of machine learning, and a representation of related emotions is presented as a response. A model of 11 different touch types was created and applied in the identification of touch of the somatosensory system. Enabling the system to include multiple types of touch, the resolution of touch representation was modified through the use of a continuous signal of high frequency, and Support-Vector Machine machine learning was applied to provide a sufficient certainty of prediction and learning with a validation accuracy of 89%. The system could thereby detect and identify 11 different types of touch and produce a related response, enabling the bi-directional touch-emotion interaction with a humanoid robot.
___
Touches learned by the model:
| Touches       | Represented as  |
| ------------- | --------------- |
| Hold          | 0               |
| Rub           | 1               |
| Pat           | 2               |
| Pick          | 3               |
| Poke          | 4               |
| Press         | 5               |
| Scratch       | 6               |
| Slap          | 7               |
| Stroke        | 8               |
| Tap           | 9               |
| Tickle        | 10              |

Emotions mapped to touches:
| Emotions      |
| ------------- |
| Sadness       |
| Anger         |
| Enjoyment     |
| Disgust       |
| Surprise      |
| Fear          |

## Hardware used
- Bare Conductive Touchboard, [found here](https://www.bareconductive.com/shop/touch-board/).
- Bare Conductive Electric Paint, [found here](https://www.bareconductive.com/shop/electric-paint-50ml/).

## Software used
Code for model is written in Python, while code for the hardware is written in C++.

Libraries used are:
- Scikit-learn (for machine learning).
- Numpy (for working in domain of linear algebra and arrays/matrices).
- Pandas (for data analysis, structure and manipulation).
- matplotlib (for visualization of data).

The machine learning is based upon Support Vector-Machine and has an SVC with:
- rbf kernel
- C = 100
- Optimized gamma
- Balanced wights

## Parts of system explained
### First of all...
...I just want to say that the code is not very neat written, but it does its job. The focus of this project has **not** been on the code.

### "Global parameters"
`N_SAMPLES` indicates the amount of samples used in order to represent a touch. Value used was 100.  
`N_ELECTRODES` indicates the amount of areas used in each sample. Value used was 12.  
`TIME_WINDOW` indicates the desired time slot of a touch. Currently set at 3.5 s.

### data_generator.py
A script for live-generating a data set. I.e. record a touch and save it.
1. Set the `ser` (serial) to the USB port of your computer.
2. Set the `TYPE_OF_TOUCH` to the type of touch you are generating.
3. Start the generator by `python data_generator.py`.
4. Start generating data representations of touches.
5. Simply stop data generation by `ctrl + C`.

The generated data is written to csv files, in this case `training_data_x.csv` and `training_data_y.csv`, where the data representation is x and the type of touch y.

Note: Modify the `N_SAMPLES`, `N_ELECTRODES` and `TIME_WINDOW` if needed.

### data_converter.py
A script used to convert the input data sent over the serial (i.e. from the Touch Board and the C++ script) to the format used in the machine learning model. Can be used on its own on a whole data set (by setting input and ouput file, and running `python data_converter.py`) or by another script by calling the `convert_data()` method (for example used in **data_generator.py** and **epi.py**).

### epi.py
A script that runs and simulates the humanoid robot in live mode. The script waits for a touch and reacts to it with the interpreted touch and triggered emotion(s); both informative and by facial expression and text answers. The output contains detailed probabilities and predictions.
1. Set the `ser` (serial) to the USB port of your computer.
2. Set the paramters used for prediction in `predict.py` (more info in **predict.py**).
3. Start the simulated humanoid robot by `python epi.py`.
4. Simply turn it off by `ctrl + C`.

Note: Modify the `N_SAMPLES` and `N_ELECTRODES` if needed.

### predict.py
A script (separated method) that is used in order take care of the predicted output from a specific input, based on the model created in training. Predictions and probabilities of all types of touch are returned.

`clf_copy` should point to the desired model, in `.pkl` format.
`x_mean` and `sigma` for normalization has to be set to the exact same as used in training. These are printed in console in training.

### printer.py
Printer contains methods that simply takes care of printing and formatting.  
For example, `print_epi(f)` prints the facial expression of Epi depending on input and `print_response(predictions, probabilities)` prints all the predicted information in a readable format.

Note: Modify the `N_SAMPLES` and `N_ELECTRODES` if needed.

### train.py
The script that handles the machine learning and training of the SVC, i.e. the model used for prediction. The ouput is the created model in `.pkl` format. Printed outputs are average accuracy of the model (from validation with the test set), as well as lowest accuracy together with its confusion matrix (to be able to quickly spot "classifying issues").

1. Set the `TEST_SIZE` to the desired size of the data set used for validation, and the `N_EOPCHS` to the desired number of epochs used in training.
2. Uncomment the `print()` call on `row 43` in order to print the `x_mean` and `sigma` that are needed in **prediction.py**.
3. Set input files of desired data set on `row 113`.
4. Simply run `train.py` to start training (and `ctrl + C` to abort it).

Note: Change `row 98` in order to output the model in another way/format than a `.pkl`.  
Note: Modify the `N_SAMPLES` and `N_ELECTRODES` if needed.

### visualizer.py
Visulizer contains methods for visualizing the data. Methods can be accessed and used from other scripts, or simply run the script on its own by `python visualizer.py`. Currently, data examples from `visualized_data_x.csv` (and `visualized_data_y.csv`) are shown.
___
### EPI_touch_analog_100
Contains the C++ script that should be uploaded on the Bare Conductive Touch Board in order to detect and sample touches from the hardware. The script begins a serial to the USB port used, and sends 12 values delimited by `,` for every sample (after a touch has been detected). The values normally range between 5-300 (where 0-5 is set as 0) and should be seen as a delta in capacitance (baseline data subtracted by filtered data). Baseline data is set at start and can differ, meaning that the environment should not have an impact.

Note: Modify the `FILL_THRESHOLD` in order to tweak the amount of empty samples needed before "ending" a touch and filling the rest (of the time window) with zeros.  
Note: Change the `delay()`on `row 114` in order to tweak the sample frequency.
