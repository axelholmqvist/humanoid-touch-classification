import csv

N_SAMPLES = 100
N_ELECTRODES = 12

def convert_dataset():
    buffer = []

    with open('training_data_x.csv', 'r') as x_file:
        x_reader = csv.reader(x_file)
        for row in x_reader:
            for i in range(N_ELECTRODES):
                for j in range(N_SAMPLES):
                    buffer.append(row[i + j*N_ELECTRODES])
            converted_row = ",".join(buffer)
            to_csv(converted_row)
            buffer = []

def to_csv(string):
    f = open('converted_training_data_x.csv','a')
    f.write(f'{string}\n')
    f.close()

def convert_data(data_vector):
    converted_data_vector = []
    for i in range(N_ELECTRODES):
        for j in range(N_SAMPLES):
            converted_data_vector.append(data_vector[i + j*N_ELECTRODES])
    return converted_data_vector

if __name__ == '__main__':
    try:
        convert_dataset()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)