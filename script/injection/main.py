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


# ==========================
# = other helper functions =
# ==========================


def reindexMinuteMap(minuteMap, amount):
    data = []
    for i in range(0, len(minuteMap)):
        data.append(minuteMap[i] + (i * amount))

    return data


# tipos de ataque
attacks = {
    "dos": 0,
    "ddos": 1
}

# vamos começar a bagaceira

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

# TODO: injetar as anomalias apenas em 1 semana para fazer os testes
# ========================================================================================================
# = mapear a cada 30 minutos para encontrar fácil as horas e injetar anomalias em intervalos de horários =
# ========================================================================================================

# TODO: definir um intervalo de tempo para injetar a anomalia e injetar apenas neste intervalo N dados anômalos em intervalos de X minutos
originalLen = len(horario)

# amount é a quantidade de dados a serem injetados por intervalo
amount = 15
# intervalo em minutos
interval = 30
# tipo de ataque
attackType = attacks['dos']

# calcular o mapeamento de index para horário de acordo com o intervalo definido
minuteMap = minuteMapper(timeMap, interval)
minuteMapLen = len(minuteMap)

# bora calcular quais serão os novos intervalos após os dados serem injetados
# afinal adicionar novos dados vai modificar os índices que correspondem ao início dos intervalos
reindexedMinuteMap = reindexMinuteMap(minuteMap, amount)


# get the maximuns and minimuns necessary to keep some data quality
packetsMin = min(pacotes)
packetsMax = max(pacotes)
bytesMin = min(_bytes)
bytesMax = max(_bytes)

# DoS: mesmo IP de origem, mesmos IPs de destino, portas distintas
# DDoS: vários IPs de origem, mesmos IPs de destino, mesma porta de origem para cada IP

# gerar um IP e uma porta padrões para o caso do ataque ser do tipo DoS
defaultIp = generateIp()
defaultPort = generatePort()

# injetar anomalias na quantidade indicada
for am in range(0, amount):
    print(defaultIp)
    print(defaultPort)
    # caos, sk8 e destruição
    for i in range(1, minuteMapLen):
        # recalcular o minuteMap toda vez pois a cada iteração
        # os indexes correspondentes a cada novo intervalo mudam
        minuteMap = minuteMapper(timeMap, interval)

        # if minuteMap[i] == 0:
        #     continue

        lastMinute = minuteMap[i-1]
        currentMinute = minuteMap[i]

        if minuteMap[i] == minuteMap[-1]:
            lastMinute = minuteMap[i]
            currentMinute = len(horario) - 1

        # ========================================================
        # = inserir dados em posiçoes aleatórias                 =
        # = porém dentro dos intervalos definidos pelo minuteMap =
        # ========================================================
        # TOTHINK: inserir respostas das requisições?
        # nos dados fica nítido que há um padrão em que há um request e então a rede envia um response
        # isto pois o IP origem de uma linha se torna o IP de destino da linha seguinte e vice-versa
        chosenOne = generateRandomInt(lastMinute, currentMinute)
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


# write it all
output = open('.test/test.csv', 'w')
output.write(
    'index,horario,ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

for i in range(0, len(horario)):
    # print('writing...')
    row = f'{i},{horario[i]},{ipOrigem[i]},{int(portaOrigem[i])},{ipDestino[i]},{int(portaDestino[i])},{int(pacotes[i])},{int(_bytes[i])}\n'
    output.write(row)


# bora limpar a sujeira
output.close()

print('finished!')

path = '.test/test.csv'
file = readFile(path)

# read all the data
index = readColumn(file, 'index')
horario = readColumn(file, 'horario')
timeMap = createDictionary(index, horario)
print(minuteMapper(timeMap, interval))
