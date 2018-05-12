import os
import subprocess
import sys
import pandas as pd
import math

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
        dictionary = dict(zip(keyColumn, valueColumn))
        # for i in range(0, len(keyColumn)):
        #     dictionary[keyColumn[i]] = valueColumn[i]
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
    # print('histograma: ', histogram)
    return histogram

# recebe um dicionário e o intervalo de tempo em minutos como parâmetros
# vai mapear o dicionário, que deve conter o índice como chave e o horário como valor
# cria uma lista com o índice do início de cada intervalo
# o intervalo será medido em minutos
# desta maneira, será possível saber de qual índice a qual índice
# se aplica a divisão no intervalo em minutos definido
def minuteMapper(dictionary, interval):
    firstKey = next(iter(dictionary))

    globalMinute = int(dictionary[firstKey].split(':')[1])

    # o primeiro valor do primeiro intervalo sempre será o primeiro item, de index 0
    intervalIndexes = [0]
    intervalCounter = 0
    
    for index in dictionary:
        minute = int(dictionary[index].split(':')[1])

        if(minute != globalMinute):
            globalMinute += 1
            intervalCounter += 1

        if(globalMinute == 60):
            globalMinute = 0

        if(intervalCounter == interval):
            intervalCounter = 0
            intervalIndexes.append(index)

    return intervalIndexes

# dá slice na lista de acordo com os valores passados e retorna o resultado
def sliceList(data, start, end):
    return data[start:end]

# calcula a probabilidade de ocorrência de cada item em um histograma
# retorna o resultado em forma de dicionário
def probability(histogram):
    total = 0
    for key in histogram:
        total += histogram[key]
    for key in histogram:
        histogram[key] /= total

    return histogram


# calcula A FUCKING ENTROPIA DE SHANNON
# A PORRA DA ENTROPIA DA INFORMAÇÃO
# FINALMENTE CARALHO PORRA
# recebe como parâmetro o dicionário com as probabilidades das chaves

def entroPy(data):
    entropy = 0
    for key in data:
        entropy += - data[key] * math.log2(data[key])
    
    return entropy

# range(start,end) vai de start até end - 1
#primeiro for para percorrer os arquivos de todos os dias
for day in range(1,32):
    file = f'../dados_rede/data/csv_data/{day}.csv'
    # file = './tests/histogramTest.csv'

    key = readColumn(file, 'index')
    value = readColumn(file, 'horario')

    dic = createDictionary(key, value)

    #mais um for, pra ir de acordo com os intervalos em minutos (1, 2, 3, 4, 5)
    #vai ser o mesmo intervalo para todas as colunas
    #mas o cálculo dos intervalos será feito uma coluna de cada vez
    #e ao final os dados serão escritos
    for minute in range(1, 6):
        vec = minuteMapper(dic, 1)

        #a lista de resultados de cada coluna vai ter o mesmo tamanho
        #visto que o CSV é padronizado

        #lista pra posterior escrita no csv
        results_ip_origem = []
        results_porta_origem = []
        results_ip_destino = []
        results_porta_destino = []

        #cria a linha do csv
        result = ''

        #mais um for, pra percorrer todos as colunas em que a entropia deve ser calculada
        entropyData = ['ip_origem', 'porta_origem', 'ip_destino', 'porta_destino']

        for column in entropyData:

            data_column = readColumn(file, column)

            count = 0
            for i in vec:
                if(i == vec[len(vec) - 1]):
                    # print('i: ', i)
                    data_histogram = createHistogram(sliceList(data_column, vec[len(vec) - 1], len(data_column)))
                    # print('intervalo:', vec[len(vec) - 1], len(ip))
                else:
                    # print('intervalo:', i, vec[count + 1])
                    data_histogram = createHistogram(sliceList(data_column, i, vec[count + 1]))

                # di = createHistogram(data)
                prob_histogram = probability(data_histogram)
                count += 1

                # print('probabilidade:', prob)

                # print(f'entropia {i}:', entroPy(prob_histogram))

                if(column == 'ip_origem'):
                    results_ip_origem.append(entroPy(prob_histogram))
                elif(column == 'porta_origem'):
                    results_porta_origem.append(entroPy(prob_histogram))
                elif(column == 'ip_destino'):
                    results_ip_destino.append(entroPy(prob_histogram))
                elif(column == 'porta_destino'):
                    results_porta_destino.append(entroPy(prob_histogram))

                # results.append(entroPy(prob_histogram))

        output = open(f'../dados_rede/data/entropy/{minute}/{day}.csv', 'w')
        output.write('index,ip_origem,porta_origem,ip_destino,porta_destino\n')

        for i in range(0,len(results_ip_origem)):
            line = ''
            line += f'{vec[i]},{results_ip_origem[i]},{results_porta_origem[i]},{results_ip_destino[i]},{results_porta_destino[i]}\n'
            
            output.write(line)

        output.close()



# entropy




# key = sliceList(key, 0, 4)
# value = sliceList(value, 0, len(value))

# di = createHistogram(value)
# prob = probability(di)

# print(prob)

# print(sliceList(key, 0, len(key)))

# dic = createDictionary(key, value)

# result = minuteMapper(dic, 1)

# print(result)

# esperado: 0 4 6 9

        
        
        

        
        
    

# key = readColumn('../dados_rede/data/csv_data/1.csv', 'ip_origem')
# histogram = createHistogram(key)
# for key, val in histogram.items():
#     print(f'{key} : {val}')


# TODO função que consegue mapear/segregar os valores de acordo com o tempo (em segundos ou minutos?)

# print(createDictionary('../dados_rede/data/csv_data/1.csv', 'index', 'horario'))

# createDictionary(readColumn('../dados_rede/data/csv_data/1.csv', 'index'), readColumn('../dados_rede/data/csv_data/1.csv', 'horario'))

# createHistogram(readColumn('../dados_rede/data/csv_data/1.csv', 'horario'))
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
