import sys
import serial
import time
import os
import csv
import numpy as np
from predict import *
from printer import *
from data_converter import *

ser = serial.Serial('/dev/cu.usbmodem141101', 115200) # <-----------* Change this to accurate port!
N_SAMPLES = 100
N_ELECTRODES = 12

def start_up():
    print_loading()
    print('Epi up and running!')
    time.sleep(0.5)
    clear()
    print_epi(-1)

def string_to_float(string_list):
    float_list = []
    float_list.append([float(i) for i in string_list])
    return float_list

def main():
    buffer = []
    t = 0
    previous_touch = ''

    while True:
        while t < N_SAMPLES:
            data = ser.readline()
            clear()
            print_epi(-1)
            if 0 <= t <= 10 or 31 <= t <= 40:
                print('.')
            if 11 <= t <= 20 or 41 <= t <= 50:
                print('..')
            if 21 <= t <= 30 or 51 <= t <= 60:
                print('...')
            string_data = data.decode().rstrip()
            buffer.append(string_data)
            t += 1
        string = ",".join(buffer)
        string_list = string.split(",")
        float_list = string_to_float(string_list)
        converted_list = convert_data(float_list[0])
        predictions, probabilities = predict(converted_list)
        clear()
        print_response(predictions, probabilities)
        buffer = []
        t = 0

if __name__ == '__main__':
    try:
        start_up()
        main()
    except KeyboardInterrupt:
        print('\nBye bye.\n')
        ser.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)