import pandas as pd
import os
import subprocess
from math import pow
from functools import reduce

column_names = ['ip_origem', 'porta_origem', 'ip_destino',
                'porta_destino', 'pacotes_ps', 'bytes_ps']


def error_file_name(minute, week, day):
    return f'../../dados_conclusoes/erros/minuto{minute}/intervalo_semana{week}/dia{day}/erro.csv'


def table_folder_name():
    return f'../../dados_conclusoes/tabelas'


def table_file_name(dimension):
    return f'{table_folder_name()}/{dimension}.xlsx'


def read_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f)


def open_file_to_write(file_path):
    return open(file_path, "w")


if not os.path.isdir(table_folder_name()):
    os.makedirs(table_folder_name())

data_frames = []
index = [1, 2, 3, 4, 5]
columns = [2, 3, 4]
for column in column_names:
    rows = []
    for minute in range(1, 6):
        row = []
        for week in range(2, 5):
            errors = []
            for day in range(1, 29):
                try:
                    data = read_file(error_file_name(minute, week, day))
                    errors.append(data[column][0])
                except:
                    continue
            errors_sum = reduce(
                lambda value, accumulator: value + accumulator, errors)
            errors_average = errors_sum / len(errors)
            row.append(errors_average)
        rows.append(row)
    data_frame = pd.DataFrame(rows, index=index, columns=columns)
    data_frame.to_excel(table_file_name(column))
    print(f'\n{column}')
    print(data_frame.min())
