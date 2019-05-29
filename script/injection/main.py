import pandas as pd
import random
import os
import subprocess


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


def minuteMapToHourMap(minuteMap):
    hourMap = []
    for i in range(0, len(minuteMap) - 1):
        if i % 2 == 0:
            hourMap.append(minuteMap[i])
    return hourMap


# índex 0 = meia-noite; index 1 = 1h da manhã; index 2 = 2h da manhã e por aí vai
# não deve-se passar 0h ou 24h como parâmetro para `finish`
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


# ataques que serão implementados: DoS e DDoS
# no DoS é utilizado apenas 1 IP e porta de origem (porta de origem é 1 só mesmo?) para vários IPs e portas de destino
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


def generateRandomInt(_min, _max):
    random.seed()

    return random.randint(_min, _max)


# tipos de ataque
attacks = {
    "dos": 0,
    "ddos": 1
}

# dia 1: sexta-feira
weeks = [
    [1, 2, 3, 4, 5, 6, 7],
    [8, 9, 10, 11, 12, 13, 14],
    [15, 16, 17, 18, 19, 20, 21],
    [22, 23, 24, 25, 26, 27, 28],
    [29, 30, 31]
]

print(weeks)

# vamos começar a bagaceira
if not os.path.isdir('../../dados_anomalos/'):
    os.makedirs('../../dados_anomalos/')

for day in weeks[0]:

    # contando de meia em meia hora fica fácil de achar os índices dos horários (meia-noite, 1h, 2h, 3h etc.)
    interval = 30

    path = f'../../dados_rede/data/csv_data/{day}.csv'
    print(f'arquivo {day}.csv')
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

    # TODO: injetar as anomalias apenas em 1 semana para fazer os testes
    # ========================================================================================================
    # = mapear a cada 30 minutos para encontrar fácil as horas e injetar anomalias em intervalos de horários =
    # ========================================================================================================

    # TODO: injetar N dados anômalos em intervalos de X minutos no intervalo escolhido???? ou só injetar loucamente sem periodicidade??????

    # amount é a quantidade de dados a serem injetados por intervalo
    amount = 10000
    # horário de início dos ataques e horário de término dos ataques, respectivamente
    # no sistema de horário 24h
    # ex: `start = 8; stop = 10` injetará anomalias entre as 8 da manhã e as 10 da manhã
    start = 8
    stop = 10
    # tipo de ataque
    attackType = attacks['dos']

    # get the maximuns and minimuns necessary to keep some data quality
    packetsMin = min(pacotes)
    packetsMax = max(pacotes)
    bytesMin = min(_bytes)
    bytesMax = max(_bytes)

    # estrutura inicial necessária para rodar direito os cript
    # cria o timeMap pra criar o minuteMap para criar o hourMap
    # o hourMap é o mapeamento em que cada valor da lista representa o índex em que determinado horário inicia
    # (o horário é no formato de 24h)
    # o intervalMap retorna sempre uma lista com 2 valores onde o primeiro é o índex do início do intervalo (por exemplo 8h da manhã)
    # o segundo valor é o índex do final do intervalo (por exemplo 10h da manhã)
    timeMap = createDictionary(index, horario)
    minuteMap = minuteMapper(timeMap, interval)
    hourMap = minuteMapToHourMap(minuteMap)
    intervalMap = hourIntervalMap(hourMap, start, stop, len(horario) - 1)

    # DoS: mesmo IP de origem, mesmos IPs de destino, portas distintas
    # DDoS: vários IPs de origem, mesmos IPs de destino, mesma porta de origem para cada IP

    # gerar um IP e uma porta padrões para o caso do ataque ser do tipo DoS
    defaultIp = generateIp()
    defaultPort = generatePort()

    # injetar anomalias na quantidade indicada dentro do intervalo indicado
    for am in range(0, amount):
        # caos, sk8 e destruição
        # ========================================================
        # = inserir dados em posiçoes aleatórias                 =
        # = porém dentro dos intervalos definidos pelo minuteMap =
        # ========================================================
        chosenOne = generateRandomInt(intervalMap[0], intervalMap[-1])

        horario = insertValueInto(horario, chosenOne, horario[chosenOne])
        # ternário é estranho em Python
        ipOrigem = insertValueInto(ipOrigem, chosenOne, generateIp(
        )) if attackType == attacks['ddos'] else insertValueInto(ipOrigem, chosenOne, defaultIp)
        portaOrigem = insertValueInto(portaOrigem, chosenOne, generatePort(
        )) if attackType == attacks['ddos'] else insertValueInto(portaOrigem, chosenOne, defaultPort)
        # pega um IP de destino já presente nos dados para que o destino seja realmente um endereço da rede
        ipDestino = insertValueInto(
            ipDestino, chosenOne, ipDestino[generateRandomInt(0, len(ipDestino) - 1)])
        portaDestino = insertValueInto(portaDestino, chosenOne, generatePort())
        pacotes = pacotesResult = insertValueInto(
            pacotes, chosenOne, generateRandomInt(packetsMin, packetsMax))
        _bytes = insertValueInto(
            _bytes, chosenOne, generateRandomInt(bytesMin, bytesMax))

        # ao final de cada operação mais um valor foi injetado nos dados
        # portanto o índex do intervalo presente no intervalMap muda
        # é só adicionar 1 ao valor final que tá tudo celto
        intervalMap[-1] += 1

    # write it all
    output = open(f'../../dados_anomalos/{day}.csv', 'w+')
    output.write(
        'index,horario,ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

    for i in range(0, len(horario)):
        # print('writing...')
        row = f'{i},{horario[i]},{ipOrigem[i]},{int(portaOrigem[i])},{ipDestino[i]},{int(portaDestino[i])},{int(pacotes[i])},{int(_bytes[i])}\n'
        output.write(row)

    # bora limpar a sujeira
    output.close()

    print(
        f'escrita do arquivo ../../dados_anomalos/{day}.csv completada com sucesso')
