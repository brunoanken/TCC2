import pandas as pd
import os
import subprocess
from math import pow

column_names = ['ip_origem', 'porta_origem', 'ip_destino',
                'porta_destino', 'pacotes_ps', 'bytes_ps']


def error_file_name(minute, week, day):
    return f'../../dados_conclusoes/erros/minuto{minute}/intervalo_semana{week}/dia{day}/erro.csv'


def table_folder_name(day, minute, week):
    return f'../../dados_conclusoes_/tabelas/{day}/minuto{minute}/intervalo_semana{week}'


def table_file_name(table_folder_name):
    return f'{table_folder_name}/tabela.csv'


def read_file(file_path):
    f = open(file_path, 'r')
    return pd.read_csv(f)


def open_file_to_write(file_path):
    return open(file_path, "w")


# row1 = ['a', 'b']
# row2 = ['c', 'd']
# rows = [row1, row2]

# index => linhas, eixo Y
# columns => COLUNAS!!!1 eixo X

# index = ['minuto1', 'minuto2']
# columns = ['semana2', 'semana3']

# df1 = pd.DataFrame(rows,
#                    index=index,
#                    columns=columns)
# print(df1)
# df1.to_excel("output.xlsx", sheet_name='cockmar')
# df2 = df1.copy()

# with pd.ExcelWriter('output.xlsx') as writer:
#     df1.to_excel(writer, sheet_name='ip_origem')
#     df2.to_excel(writer, sheet_name="porta_origem")

for day in range(1, 29):
    dataframes = []
    for column in column_names:
        rows = []
        index = []
        columns = []
        for minute in range(1, 6):
            row = []
            index.append(minute)
            for week in range(2, 5):
                columns.append(week)
                data = read_file(error_file_name(minute, week, day))
                row.append(data[column][0])
            rows.append(row)
    print(dataframes)
