import pandas as pd
import os
import subprocess

column_names = ['ip_origem', 'porta_origem', 'ip_destino',
                'porta_destino', 'pacotes_ps', 'bytes_ps']


def entropy_attack_file_name(attack, minute, day):
    return f'../../dados_anomalos/entropy/{attack}/{minute}/{day}.csv'


def entropy_file_name(minute, day):
    return f'../../dados_rede/data/entropy/{minute}/{day}.csv'


def baseline_file_name(minute, week, day):
    return f'../../dados_rede/data/baseline/minuto{minute}/intervalo_semana{week}/dia{day}/baseline.csv'


def difference_file_name(day):
    return f'../../dados_conclusoes/difference/{day}.xlsx'


def read_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f)


def read_baseline_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f, names=column_names)


def open_file_to_write(file_path):
    return open(file_path, "w")


def hour_to_minutes(hour, interval):
    return hour * 60 / interval


attacks = ["dos", "ddos"]

######################
minute_interval = 5  #
week_inteval = 2     #
######################

# intervalo de ataque
# hora de início e hora de término, formato 24h
start_hour = 8
stop_hour = 10

start = hour_to_minutes(start_hour, minute_interval)
stop = hour_to_minutes(stop_hour, minute_interval)

start_index = int(start - 1)
stop_index = int(stop - 1)
total = stop_index - start_index

difference_folder = '../../dados_conclusoes/difference'
if not os.path.isdir(difference_folder):
    os.makedirs(difference_folder)

for day in range(1, 8):
    rows = []

    for attack in attacks:

        baseline = read_baseline_file(
            baseline_file_name(minute_interval, week_inteval, day))
        attack_entropy = read_file(
            entropy_attack_file_name(attack, minute_interval, day))
        row = []

        for column in column_names:
            baseline_sum = 0
            attack_sum = 0

            for index in range(start_index, stop_index + 1):
                baseline_sum += baseline[column][index]
                attack_sum += attack_entropy[column][index]

            baseline_average = baseline_sum / total
            attack_average = attack_sum / total

            difference = (attack_average - baseline_average) / baseline_average
            percentage = difference * 100
            row.append(percentage)

        rows.append(row)

    data_frame = pd.DataFrame(rows, index=attacks, columns=column_names)
    data_frame.to_excel(difference_file_name(day))
    print(f'\ndia: {day}')
    print(data_frame)
