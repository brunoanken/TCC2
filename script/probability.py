import os
import subprocess
import sys
import pandas as pd

os.chdir("./../dados_rede/data/csv_data")

file = '1.csv'

f=open(file,'r')

df = pd.read_csv(file)

# squeeze : boolean, default False => If the parsed data only contains one column then return a Series

histogram = {}

def insertInDict(value):
    if value in histogram:
        histogram[value] += 1
    else:
        histogram[value] = 1
        # histogram[value] += 1

columnList = df['ip_destino'].apply(insertInDict)

output = open('histogramTest.csv', 'w')

for key, value in histogram.items():
    output.write(f'{key},{value}\n')

output.close()

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
