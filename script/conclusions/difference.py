import pandas as pd
import os
import subprocess

column_names = ['ip_origem', 'porta_origem', 'ip_destino',
                'porta_destino', 'pacotes_ps', 'bytes_ps']


def entropy_file_name(minute, day):
    return f'../../dados_rede/data/entropy/{minute}/{day}.csv'


def baseline_file_name(minute, week, day):
    return f'../../dados_rede/data/baseline/minuto{minute}/intervalo_semana{week}/dia{day}/baseline.csv'


def error_folder_name(minute, week, day):
    return f'../../dados_conclusoes/erros/minuto{minute}/intervalo_semana{week}/dia{day}'


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


def hour_to_minutes(hour, interval):
    return hour * 60 / interval

# def createDictionary(keyColumn, valueColumn):
#     if(len(keyColumn) == len(valueColumn)):
#         dictionary = dict(zip(keyColumn, valueColumn))
#         return dictionary
#     else:
#         print('ERRO: listas com tamanhos diferentes')


# def minuteMapper(dictionary, interval):
#     firstKey = next(iter(dictionary))

#     globalMinute = int(dictionary[firstKey].split(':')[1])

#     intervalIndexes = [0]
#     intervalCounter = 0

#     for index in dictionary:
#         minute = int(dictionary[index].split(':')[1])

#         if(minute != globalMinute):
#             globalMinute += 1
#             intervalCounter += 1

#         if(globalMinute == 60):
#             globalMinute = 0

#         if(intervalCounter == interval):
#             intervalCounter = 0
#             intervalIndexes.append(index)

#     return intervalIndexes


# def minuteMapToHourMap(minuteMap):
#     hourMap = []
#     for i in range(0, len(minuteMap) - 1):
#         if i % 2 == 0:
#             hourMap.append(minuteMap[i])
#     return hourMap


# def hourIntervalMap(hourMap, start, finish, lastIndex):
#     if (finish <= start):
#         raise Exception(
#             "valor do horário de fim do intervalo superior ou igual ao valor do horário de início")

#     intervalMap = []
#     intervalMap.append(hourMap[start])

#     if finish == 24:
#         intervalMap.append(hourMap[lastIndex])
#     else:
#         intervalMap.append(hourMap[finish])

#     return intervalMap


weeks = [
    [1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19, 20, 21],
    [22, 23, 24, 25, 26, 27, 28],
    [29, 30, 31]
]

# intervalo de minutos
interval = 1

# intervalo de ataque
# hora de início e hora de término, formato 24h
start = 8
stop = 10

start_minute_interval = hour_to_minutes(start, interval)
stop_minute_interval = hour_to_minutes(start, interval)

baseline = read_baseline_file(baseline_file_name(1, 2, 1))
print(len(baseline[column_names[0]]))
