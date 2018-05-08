import os
import subprocess
import sys
import pandas as pd

os.chdir("../dados_rede/data/csv_data")

# target_file = pd.read_csv('1.csv')
# dictionary = target_file.
# saved_column = target_file.horario.toList()

df = pd.read_csv('1.csv', usecols=['horario', 'ip_origem'])
result = df.to_dict(orient='records')

print(result)


# myList = list()
# myList.append('buceta de anao')
# myList.append('piroca de gigante')
# print(myList)

# print(saved_column)
# print('length:', len(saved_column))