import pandas as pd
import os
import subprocess
from math import pow

column_names = ['ip_origem', 'porta_origem', 'ip_destino',
                'porta_destino', 'pacotes_ps', 'bytes_ps']

attack_types = {
    "dos": "dos",
    "ddos": "ddos"
}


def entropy_file_name(attack, minute, day):
    return f'../../dados_anomalos/entropy/{attack}/{minute}/{day}.csv'


def baseline_file_name(minute, week, day):
    return f'../../dados_rede/data/baseline/minuto{minute}/intervalo_semana{week}/dia{day}/baseline.csv'


def error_folder_name(attack, minute, week, day):
    return f'../../dados_conclusoes/{attack}/erros/minuto{minute}/intervalo_semana{week}/dia{day}'


def error_file_name(error_folder_name):
    return f'{error_folder_name}/erro.csv'


def read_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f)


def read_baseline_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f, names=column_names)


def open_file_to_write(file_path):
    return open(file_path, "w")


def calculate_square_error(real_value, baseline_value):
    difference = real_value - baseline_value
    square_error = pow(difference, 2)
    return square_error


attack = attack_types["ddos"]


for minute_interval in range(1, 6):

    for week_interval in range(2, 5):

        for day in range(1, 8):
            baseline_data = read_baseline_file(baseline_file_name(
                minute_interval, week_interval, day))
            entropy_data = read_file(
                entropy_file_name(attack, minute_interval, day))

            average_errors = {}

            for column in column_names:
                data_baseline = baseline_data[column]
                data_entropy = entropy_data[column]
                data_len = len(data_baseline)
                square_error_accumulator = 0

                for item in range(data_len):
                    square_error_accumulator += calculate_square_error(
                        data_entropy[item], data_baseline[item])

                average_errors[column] = square_error_accumulator / data_len

            output_path = error_folder_name(attack,
                                            minute_interval, week_interval, day)

            if not os.path.isdir(output_path):
                os.makedirs(output_path)
            output = open_file_to_write(error_file_name(output_path))

            output.write(
                'ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

            line = ''
            for column in column_names:
                if (column == "bytes_ps"):
                    line += f'{average_errors[column]}\n'
                else:
                    line += f'{average_errors[column]},'
            output.write(line)
            print(
                f'FINISH writing file {error_file_name(output_path)}')
            output.close()
