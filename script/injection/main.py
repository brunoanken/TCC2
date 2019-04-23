import pandas as pd
import random

# ========================================
# files and lists manipulation functions =
# ========================================


def readFile(filePath):
    f = open(filePath, 'r')
    return pd.read_csv(f)


def readColumn(file, columnName):
    return file[columnName].tolist()


def sliceList(data, start, end):
    return data[start:end]


def createDictionary(keyColumn, valueColumn):
    if(len(keyColumn) == len(valueColumn)):
        dictionary = dict(zip(keyColumn, valueColumn))
        return dictionary
    else:
        print('ERRO: listas com tamanhos diferentes')


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


# TODO: pegar a função que faz o mapeamento de index para minutos
# fazer outra função que vai modificar o resultado da primeira de acordo
# com novos dados sendo injetados pois isto modifica o valor dos índices que correspondem aos minutos


# ataques que serão implementados: DoS e DDoS
# no DoS é utilizado apenas 1 IP e porta de origem para vários IPs e portas de destino
# no DDoS são vários IPs e portas de origem para vários IPs e portas de destino

# TODO: maximum bytes and packets in a file and use it those values as a limit in data generation
# TODO: checar os IPs de destino presentes no arquivo e utilizar apenas estes valores

# ========================================
# data generation functions              =
# ========================================

def insertValueInto(data, position, value):
    prePosition = sliceList(data, 0, position)
    posPosition = sliceList(data, position, len(data))
    prePosition.append(value)
    return prePosition + posPosition


def generateIp():
    _min = int(0)
    _max = int(255)

    random.seed()

    return f'{random.randint(_min, _max)}.{random.randint(_min, _max)}.{random.randint(_min, _max)}.{random.randint(_min, _max)}'


def generatePort():
    _min = int(0)
    _max = int(65535)

    random.seed()

    return random.randint(_min, _max)


def generatePacketsOrBytes(_min, _max):
    random.seed()

    return random.randint(_min, _max)


path = '.test/1.csv'
file = readFile(path)

# read all the data
index = readColumn(file, 'index')
horario = readColumn(file, 'horario')
ipOrigem = readColumn(file, 'ip_origem')
portaOrigem = readColumn(file, 'porta_origem')
ipDestino = readColumn(file, 'ip_destino')
portaDestino = readColumn(file, 'porta_destino')
pacotes = readColumn(file, 'pacotes')
_bytes = readColumn(file, 'bytes')

timeMap = createDictionary(index, horario)

# get the maximuns and minimuns necessary to keep some data quality
packetsMax = max(pacotes)
packetsMin = min(pacotes)
bytesMax = max(_bytes)
bytesMin = min(_bytes)

# generate and insert values
horarioResult = insertValueInto(horario, 2, 'HorarioResult')
ipOrigemResult = insertValueInto(ipOrigem, 2, generateIp())
portaOrigemResult = insertValueInto(portaOrigem, 2, generatePort())
ipDestinoResult = insertValueInto(ipDestino, 2, 'IpDestinoResult')
portaDestinoResult = insertValueInto(portaDestino, 2, generatePort())
pacotesResult = insertValueInto(
    pacotes, 2, generatePacketsOrBytes(packetsMin, packetsMax))
_bytesResult = insertValueInto(
    _bytes, 2, generatePacketsOrBytes(bytesMin, bytesMax))

# write it all
output = open('.test/test.csv', 'w')
output.write(
    'index,horario,ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

# for i in range(0, len(horarioResult)):
for i in range(0, 5):
    print('writing...')
    print(i)
    row = ''
    row += f'{i},{horarioResult[i]},{ipOrigemResult[i]},{int(portaOrigemResult[i])},{ipDestinoResult[i]},{int(portaDestinoResult[i])},{int(pacotesResult[i])},{int(_bytesResult[i])}\n'
    output.write(row)

# bora limpar a sujeira
output.close()

print('finished!')
