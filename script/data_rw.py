import os
import subprocess
import sys

# DEFINA O DIA QUE VOCE DESEJA INICIAR O PROCESSAMENTO
diaInicio = 1

# DEFINA O ÚLTIMO DIA A SER PROCESSADO (na realidade é o último dia + 1)
diaTermino = 32

# coloque o endereço do diretório onde se encontram os dados
os.chdir("../dados_rede/data")
# diretório para guardar os dados em formato CSV
os.makedirs('csv_data')


def get_key(line):
    horario = line.split(",")[0]
    horas = int(horario.split(':')[0])
    minutos = int(horario.split(':')[1])
    segundos = int(horario.split(':')[2])
    return horas*3600+minutos*60+segundos


for dia in range(diaInicio, diaTermino):

    fileName = f'{dia}.txt'
    file = open(fileName, 'w+')

    c_minutos = 0
    c_horas = 0

    while c_horas <= 23:
        arquivo = f'{dia:02}/nfcapd.201303{dia:02}{c_horas:02}{c_minutos:02}'
        sys.stdout.write(arquivo + "\n")
        try:
            proc = subprocess.Popen(['nfdump', '-r', arquivo],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            flag = 1
            for line in proc.stdout:
                if flag == 1:
                    flag = 2
                else:
                    st = line.split(' ')
                    if st[0] == 'Summary:' or st[0] == 'Time' or st[0] == 'Total':
                        break
                    horario = st[1].split('.')
                    # Hora da marretada
                    # O numero de espacos entre o Protocolo e o endereco de origem e variavel #fodeu
                    # Workaround Time
                    if st[3] != 'TCP' and st[3] != 'UDP' and st[3] != 'ICMP' and st[3] != 'ICMP6' and st[3] != 'IPv6' and st[3] != 'GRE':
                        index = 4
                        while st[index] != 'TCP' and st[index] != 'UDP' and st[index] != 'ICMP' and st[index] != 'ICMP6' and st[index] != 'IPv6' and st[index] != 'GRE':
                            index += 1
                        index += 1
                    else:
                        if st[3] == 'ICMP6':
                            continue
                        index = 4
                    while st[index] == '' or st[index] == '->':
                        index += 1
                    # Invocando o Deus da Gambi para Tratar Endereços IPv6
                    origem = st[index]
                    o_splitted = origem.split(':')
                    if len(o_splitted) > 2:
                        porta_origem = origem.split(
                            '.')[len(origem.split('.'))-1]
                        ip_origem = ''
                        for ele in origem.split('.'):
                            if ele != porta_origem:
                                ip_origem += ele
                    else:
                        ip_origem = origem.split(':')[0]
                        porta_origem = origem.split(':')[1]
                    index += 1
                    while st[index] == '' or st[index] == '->':
                        index += 1
                    destino = st[index]
                    d_splitted = destino.split(':')
                    if len(d_splitted) > 2:
                        porta_destino = destino.split(
                            '.')[len(destino.split('.'))-1]
                        ip_destino = ''
                        for ele in destino.split('.'):
                            if ele != porta_destino:
                                ip_destino += ele
                    else:
                        ip_destino = destino.split(':')[0]
                        porta_destino = destino.split(':')[1]
                    index += 1
                    while st[index] == '' or st[index] == '->':
                        index += 1
                    pacotes = st[index]
                    index += 1
                    while st[index] == '' or st[index] == '->':
                        index += 1
                    bytes = st[index]
                    # sys.stdout.write("x\n")
                    file.write("%s,%s,%s,%s,%s,%s,%s\n" % (
                        horario[0], ip_origem, porta_origem, ip_destino, porta_destino, pacotes, bytes))
        except:
            print(f'ERRO NO ARQUIVO {arquivo}')
            # TODO escrever os erros em outro arquivo para averiguar os mesmos
        c_minutos += 5
        if c_minutos == 60:
            c_minutos = 0
            c_horas += 1

    file.close()

    # Ordenando o arquivo
    cabecalho = ''
    finalFileName = f'csv_data/{dia}.csv'
    output = open(finalFileName, 'w+')
    all_lines = open(fileName, 'r')
    output.write(
        'index,horario,ip_origem,porta_origem,ip_destino,porta_destino,pacotes,bytes\n')
    indexGeral = 0
    for line in sorted(all_lines, key=get_key):
        output.write(f'{indexGeral},{line}')
        indexGeral += 1

    output.close()
    all_lines.close()

    os.remove(fileName)

proc.wait
