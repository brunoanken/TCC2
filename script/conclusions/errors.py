import pandas as pd
import os
import subprocess

column_names = ['ip_origem', 'porta_origem', 'ip_destino',
                'porta_destino', 'pacotes_ps', 'bytes_ps']


def baseline_file_name(minute, week, day):
    return f'../../dados_rede/data/baseline/minuto{minute}/intervalo_semana{week}/dia{day}/baseline.csv'


def error_file_name(minute, week, day):
    return f'../../dados_conclusoes/erros/minuto{minute}/intervalo_semana{week}/dia{day}/erro.csv'


def read_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f)


def read_headerless_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f, names=column_names)


file = read_headerless_file(baseline_file_name(1, 2, 1))
print(file)
