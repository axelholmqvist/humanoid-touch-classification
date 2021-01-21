import sys
import serial
import time
import os
import csv
from data_converter import *

ser = serial.Serial('/dev/cu.usbmodem141101', 115200) # <-----------* Change this to accurate port!
N_SAMPLES = 100
N_ELECTRODES = 12
TIME_WINDOW = 3.5

TYPE_OF_TOUCH = 10 # <-----------* Set the type of touch that you are training.

def main():
    buffer = []
    t = 0

    while True:
        print('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
        print('Awaits new input data...')
        print('\nTime:\tInput data:')
        print('┌───────────────────────────────')
        while t < N_SAMPLES:
            data = ser.readline()
            string_data = data.decode().rstrip()
            buffer.append(string_data)
            time_stamp = '{:0.2f}'.format(t/(N_SAMPLES / TIME_WINDOW))
            print(f'│ {time_stamp}\t{string_data}')
            t += 1
        string = ",".join(buffer)
        string_list = string.split(",")
        int_list = list(map(int, string_list))
        converted_int_list = convert_data(int_list)
        final_data_entry = ",".join(map(str, converted_int_list))
        print('└───────────────────────────────')
        print(f'\n┌ Data added to training dataset as:\n└─> {final_data_entry}\n')
        x_to_csv(final_data_entry, 'training_data_x.csv')
        y_to_csv(TYPE_OF_TOUCH, 'training_data_y.csv')
        buffer = []
        t = 0

def to_csv(string, output):
    f = open(output,'a')
    f.write(f'\n{string}')
    f.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nData generator terminated. Good luck with the data!\n')
        ser.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)