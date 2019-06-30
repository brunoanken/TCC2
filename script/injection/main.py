import pandas as pd
import random
import os
import subprocess


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


def minuteMapToHourMap(minuteMap):
    hourMap = []
    for i in range(0, len(minuteMap) - 1):
        if i % 2 == 0:
            hourMap.append(minuteMap[i])
    return hourMap


def hourIntervalMap(hourMap, start, finish, lastIndex):
    if (finish <= start):
        raise Exception(
            "valor do horário de fim do intervalo superior ou igual ao valor do horário de início")

    intervalMap = []
    intervalMap.append(hourMap[start])

    if finish == 24:
        intervalMap.append(hourMap[lastIndex])
    else:
        intervalMap.append(hourMap[finish])

    return intervalMap


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


def generateRandomInt(_min, _max):
    random.seed()

    return random.randint(_min, _max)


attacks = {
    "dos": 0,
    "ddos": 1
}

weeks = [
    [1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19, 20, 21],
    [22, 23, 24, 25, 26, 27, 28],
    [29, 30, 31]
]

if not os.path.isdir('../../dados_anomalos/dos'):
    os.makedirs('../../dados_anomalos/dos')

if not os.path.isdir('../../dados_anomalos/ddos'):
    os.makedirs('../../dados_anomalos/ddos')

for day in weeks[0]:

    interval = 30

    path = f'../../dados_rede/data/csv_data/{day}.csv'
    print(f'arquivo {day}.csv')
    file = readFile(path)

    index = readColumn(file, 'index')
    horario = readColumn(file, 'horario')
    ipOrigem = readColumn(file, 'ip_origem')
    portaOrigem = readColumn(file, 'porta_origem')
    ipDestino = readColumn(file, 'ip_destino')
    portaDestino = readColumn(file, 'porta_destino')
    pacotes = readColumn(file, 'pacotes')
    _bytes = readColumn(file, 'bytes')

    amount = 1000
    start = 8
    stop = 10
    attackType = attacks['dos']

    packetsMin = min(pacotes)
    packetsMax = max(pacotes)
    bytesMin = min(_bytes)
    bytesMax = max(_bytes)

    timeMap = createDictionary(index, horario)
    minuteMap = minuteMapper(timeMap, interval)
    hourMap = minuteMapToHourMap(minuteMap)
    intervalMap = hourIntervalMap(hourMap, start, stop, len(horario) - 1)

    defaultIp = generateIp()
    defaultPort = generatePort()

    for am in range(0, amount):
        print(am)
        chosenOne = generateRandomInt(intervalMap[0], intervalMap[-1])

        horario = insertValueInto(horario, chosenOne, horario[chosenOne])
        ipOrigem = insertValueInto(ipOrigem, chosenOne, generateIp(
        )) if attackType == attacks['ddos'] else insertValueInto(ipOrigem, chosenOne, defaultIp)
        portaOrigem = insertValueInto(portaOrigem, chosenOne, generatePort(
        )) if attackType == attacks['ddos'] else insertValueInto(portaOrigem, chosenOne, defaultPort)
        ipDestino = insertValueInto(
            ipDestino, chosenOne, ipDestino[generateRandomInt(0, len(ipDestino) - 1)])
        portaDestino = insertValueInto(portaDestino, chosenOne, generatePort())
        pacotes = pacotesResult = insertValueInto(
            pacotes, chosenOne, generateRandomInt(packetsMin, packetsMax))
        _bytes = insertValueInto(
            _bytes, chosenOne, generateRandomInt(bytesMin, bytesMax))

        intervalMap[-1] += 1

    typeToSave = "ddos" if attackType == attacks['ddos'] else "dos"
    output = open(f'../../dados_anomalos/{typeToSave}/{day}.csv', 'w+')
    output.write(
        'index,horario,ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

    for i in range(0, len(horario)):
        row = f'{i},{horario[i]},{ipOrigem[i]},{int(portaOrigem[i])},{ipDestino[i]},{int(portaDestino[i])},{int(pacotes[i])},{int(_bytes[i])}\n'
        output.write(row)

    output.close()

    print(
        f'escrita do arquivo ../../dados_anomalos/{day}.csv completada com sucesso')
