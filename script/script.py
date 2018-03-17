import os
import subprocess
import sys
import csv

# TODO pensar na segurança dos arquivos criados
# AFINAL DE CONTAS O SEU TCC É NA ÁREA DE SEGURANÇA, NÉ...

# vai ao diretório em que estão localizados os arquivos nfcapd
os.chdir("/home/anken/Documents/TCC2/dados_rede/data/01")

# realiza o comando de leitura do arquivo
proc = subprocess.Popen(['nfdump', '-R', 'nfcapd.201303012355', '-o', 'extended'],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

#ISSO DEU CERTO AHEUEAHAEUODHNSAOUDGWABIUYDPAGDFSAPIDUŚAGHDUIWGDPWAISA
def readNfcapd():
    #cria um arquivo 
    test = open('test2.txt', 'w')
    #escreve o resultado da leitura de proc em um .txt
    for line in proc.stdout:
        sys.stdout.write(line)
        test.write(line)

readNfcapd()

# ** -- **
# CSV

# test = open('test2.txt', 'r')
# out_csv = csv.writer(open('out_csv.csv', 'wb'))

# file_string = test.read()
# file_list = file_string.split(' ')

# out_csv.writerows(test)