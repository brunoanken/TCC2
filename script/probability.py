import os
import subprocess
import sys
import pandas as pd

# lê a coluna passada como argumento e retorna seus valores em uma lista
def readColumn(filePath, columnName):
    f=open(filePath,'r')
    data = pd.read_csv(f)
    return data[columnName].tolist()

# lê as duas colunas passadas como argumento e retorna seus valores
def readColumns(filePath, firstColumnName, secondColumnName):
    f=open(filePath,'r')
    data = pd.read_csv(f)
    return data[[firstColumnName, secondColumnName]]

# cria um dicionário usando uma lista como chave e outra lista como valor
def createDictionary(keyColumn, valueColumn):
    if(len(keyColumn) == len(valueColumn)):
        dictionary = {}
        for i in range(0, len(keyColumn)):
            dictionary[keyColumn[i]] = valueColumn[i]
        return dictionary
    else:
        print('ERRO: listas com tamanhos diferentes')

# cria um histograma dos valores da lista passada como parâmetro
def createHistogram(data):
    histogram = {}
    for value in data:
        if value in histogram:
            histogram[value] += 1
        else:
            histogram[value] = 1
    return histogram

# TODO função que consegue mapear/segregar os valores de acordo com o tempo (em segundos ou minutos?)

# print(createDictionary('../dados_rede/data/csv_data/1.csv', 'index', 'horario'))

# createDictionary(readColumn('../dados_rede/data/csv_data/1.csv', 'index'), readColumn('../dados_rede/data/csv_data/1.csv', 'horario'))

createHistogram(readColumn('../dados_rede/data/csv_data/1.csv', 'horario'))
# path = '../dados_rede/data/csv_data/'
# file = '1.csv'

# histogram = {}

# f=open(f'{path}{file}','r')
# data = pd.read_csv(f)

# def checkTime(horario):
#     tempo = horario.split(':')
#     print(tempo)

# data_index_originIp = data[['horario', 'ip_origem']].to_dict()

# print(data_index_originIp)







# def insertInDict(value):
    # if value in histogram:
    #     histogram[value] += 1
    # else:
    #     histogram[value] = 1

# columnList = df['ip_origem'].apply(insertInDict)

# output = open('histogramTest.csv', 'w')

# for key, value in histogram.items():
#     output.write(f'{key},{value}\n')

# output.close()








# first = df['second'].tolist()
# first = df['second'].tolist()
# print(first)
# print(len(first),'\n')

# for fuck in first:
#     print(fuck)

# df = pd.read_csv(file, usecols=['first'])
# print(df.values) # tere çante o resultado

# column = df['first'].tolist()
# histogram = {}

# for item in column:
#     histogram[]

# if 'a' in histogram:
#     print('deu bom')
# else:
#     histogram['a'] = 0
#     print('deu ruim')

# if 'a' in histogram:
#     print('deu bom 2')
#     histogram['a'] += 1
#     print(histogram['a'])
# else:
#     print('deu ruim 2')
