import pandas as pd
import os
import subprocess

columnNames = ['ip_origem', 'porta_origem', 'ip_destino',
               'porta_destino', 'pacotes_ps', 'bytes_ps']


def readFile(filePath):
    f = open(filePath, 'r')
    return pd.read_csv(f)


def readFileWithoutHeader(filePath):
    f = open(filePath, 'r')
    return pd.read_csv(f, names=columnNames)


file = readFileWithoutHeader(
    '../../dados_rede/data/baseline/minuto1/intervalo_semana2/dia1/baseline.csv')
print(file)
