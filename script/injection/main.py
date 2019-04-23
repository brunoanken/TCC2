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


# ataques que serão implementados: DoS e DDoS
# no DoS é utilizado apenas 1 IP e porta de origem para vários IPs e portas de destino
# no DDoS são vários IPs e portas de origem para vários IPs e portas de destino

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


# ========================================
# time generation functions              =
# ========================================


def generateSecond():
    secondMin = 0
    secondMax = 59
    random.seed()

    return random.randint(secondMin, secondMax)


def generateMinute(minuteMin, minuteMax):
    random.seed()

    return random.randint(minuteMin, minuteMax)


def generateFormattedMinute(minuteMin, minuteMax):
    return f'{generateMinute(minuteMin, minuteMax):02d}'


def generateTimestamp(hour, minuteMin, minuteMax):
    return f'{hour}:{generateFormattedMinute(minuteMin, minuteMax)}:{generateSecond()}'

# ==========================
# = other helper functions =
# ==========================


def reindexMinuteMap(minuteMap, amount):
    data = []
    for i in range(0, len(minuteMap)):
        data.append(minuteMap[i] + (i * amount))

    return data

# =============================


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

originalLen = len(horario)
# =========================
# =                       =
# =========================

# gerar e inserir apenas dados nos últimos momentos do minuto? No comecinho?
# fica padronizado, mas isto apenas se realmente a ordem do timestamp importar neste caso
# dá pra inserir no começo e no fim...

# primeiro vamos fazer um teste para conseguir colocar 1 linha nova a cada 30 minutos
# apenas no final do arquivo (time stamp sempre do final do momento)
amount = 2
interval = 30

# calcular o mapeamento de index para horário de acordo com o intervalo definido
minuteMap = minuteMapper(timeMap, interval)
# adicionar o index do último instante do arquivo pois nele também deverão ser adicionados novos dados
minuteMap.append(index[-1])

# bora calcular quais serão os novos intervalos após os dados serem injetados
# afinal adicionar novos dados vai modificar os índices que correspondem ao início dos intervalos
reindexedMinuteMap = reindexMinuteMap(minuteMap, amount)

# estou adicionando apenas nos últimos instantes do minuto
# então não é necessário o primeiro item, que sempre será o primeiro instante dos arquivos
minuteMap.pop(0)
reindexedMinuteMap.pop(0)

print(minuteMap)
print(reindexedMinuteMap)

# get the maximuns and minimuns necessary to keep some data quality
packetsMin = min(pacotes)
packetsMax = max(pacotes)
bytesMin = min(_bytes)
bytesMax = max(_bytes)


# injetar anomalias na quantidade indicada
# (se colocar este for antes do for do minuteMap a injeção de anomalias fica mais espalhada)
# (se deixar depois ele cola tudo junto no final dos minutos)
# (mas aí fica foda pra setar O HORÁRIO...)
# (mas tem uma gambi bonita: pegar o mesmo horário que o logo antes ou depois da posição em que o dado será injetado)
for am in range(0, amount):
    # caos, sk8 e destruição
    for minute in minuteMap:

        # inserir os dados
        horario = insertValueInto(horario, minute, horario[minute])
        ipOrigem = insertValueInto(ipOrigem, minute, generateIp())
        portaOrigem = insertValueInto(portaOrigem, minute, generatePort())
        ipDestino = insertValueInto(ipDestino, minute, generateIp())
        portaDestino = insertValueInto(portaDestino, minute, generatePort())
        pacotes = pacotesResult = insertValueInto(
            pacotes, minute, generatePacketsOrBytes(packetsMin, packetsMax))
        _bytes = insertValueInto(
            _bytes, minute, generatePacketsOrBytes(bytesMin, bytesMax))

        if minute == index[-1]:
            horario.append(horario[-1])
            ipOrigem.append(generateIp())
            portaOrigem.append(generatePort())
            ipDestino.append(generateIp())
            portaDestino.append(generatePort())
            pacotes.append(generatePacketsOrBytes(packetsMin, packetsMax))
            _bytes.append(generatePacketsOrBytes(bytesMin, bytesMax))

finalLen = len(horario)
print(finalLen - originalLen)
# write it all
output = open('.test/test.csv', 'w')
output.write(
    'index,horario,ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

for i in range(0, len(horario)):
    # print('writing...')
    # print(i)
    row = ''
    row += f'{i},{horario[i]},{ipOrigem[i]},{int(portaOrigem[i])},{ipDestino[i]},{int(portaDestino[i])},{int(pacotes[i])},{int(_bytes[i])}\n'
    output.write(row)


# bora limpar a sujeira
output.close()

print('finished!')
