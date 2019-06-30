import pandas as pd
import os
import subprocess
from math import pow


def baseline_file_name(minute, week, day):
    return f'../../dados_rede/data/baseline/minuto{minute}/intervalo_semana{week}/dia{day}/baseline.csv'


def error_folder_name(minute, week, day):
    return f'../../dados_conclusoes/erros/minuto{minute}/intervalo_semana{week}/dia{day}'


def error_file_name(error_folder_name):
    return f'{error_folder_name}/erro.csv'
