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


def insertValueInto(data, position, value):
    prePosition = sliceList(data, 0, position)
    posPosition = sliceList(data, position, len(data))
    prePosition.append(value)
    return prePosition + posPosition


# ataques que serão implementados: DoS e DDoS
# no DoS é utilizado apenas 1 IP e porta de origem para vários IPs e portas de destino
# no DDoS são vários IPs e portas de origem para vários IPs e portas de destino

# TODO: maximum bytes and packets in a file and use it those values as a limit in data generation
# TODO: checar os IPs de destino presentes no arquivo e utilizar apenas estes valores

# ========================================
# data generation functions              =
# ========================================


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

horario = readColumn(file, 'horario')
horarioResult = insertValueInto(horario, 2, 'HorarioResult')
ipOrigem = readColumn(file, 'ip_origem')
ipOrigemResult = insertValueInto(ipOrigem, 2, generateIp())
portaOrigem = readColumn(file, 'porta_origem')
# print(min(portaOrigem))
portaOrigemResult = insertValueInto(portaOrigem, 2, generatePort())
ipDestino = readColumn(file, 'ip_destino')
ipDestinoResult = insertValueInto(ipDestino, 2, 'IpDestinoResult')
portaDestino = readColumn(file, 'porta_destino')
# print(min(portaDestino))
portaDestinoResult = insertValueInto(portaDestino, 2, generatePort())
pacotes = readColumn(file, 'pacotes')
# print(max(pacotes))
packetsMax = max(pacotes)
packetsMin = min(pacotes)
pacotesResult = insertValueInto(
    pacotes, 2, generatePacketsOrBytes(packetsMin, packetsMax))
_bytes = readColumn(file, 'bytes')
# print(min(_bytes))
bytesMax = max(_bytes)
bytesMin = min(_bytes)
_bytesResult = insertValueInto(
    _bytes, 2, generatePacketsOrBytes(bytesMin, bytesMax))

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
