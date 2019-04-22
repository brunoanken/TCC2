import pandas as pd

# ========================================
# files and lists manipulation functions =
# ========================================


def readFile(filePath):
    f = open(filePath, 'r')
    return pd.read_csv(f)


def readColumn(file, columnName):
    return file[columnName].tolist()


def insertValueInto(data, position, value):
    prePosition = data[0:position]
    posPosition = data[position:len(data)]
    prePosition.append(value)
    return prePosition + posPosition

# ========================================
# files and lists manipulation functions =
# ========================================


file = readFile('.test/1.csv')

horario = readColumn(file, 'horario')
horarioResult = insertValueInto(horario, 2, 'HorarioResult')
ipOrigem = readColumn(file, 'ip_origem')
ipOrigemResult = insertValueInto(ipOrigem, 2, 'IPOrigemResult')
portaOrigem = readColumn(file, 'porta_origem')
portaOrigemResult = insertValueInto(portaOrigem, 2, 'PortaOrigemResult')
ipDestino = readColumn(file, 'ip_destino')
ipDestinoResult = insertValueInto(ipDestino, 2, 'IpDestinoResult')
portaDestino = readColumn(file, 'porta_destino')
portaDestinoResult = insertValueInto(portaDestino, 2, 'PortaDestinoResult')
pacotes = readColumn(file, 'pacotes')
pacotesResult = insertValueInto(pacotes, 2, 'Pacotassos')
_bytes = readColumn(file, 'bytes')
_bytesResult = insertValueInto(_bytes, 2, 'Bytes demais')

output = open('.test/test.csv', 'w')
output.write(
    'index,ip_origem,porta_origem,ip_destino,porta_destino,pacotes_ps,bytes_ps\n')

for i in range(0, len(horarioResult)):
    print('writing...')
    print(i)
    row = f'{i},{horarioResult},{ipOrigemResult[i]},{portaOrigemResult[i]},{ipDestinoResult[i]},{portaDestinoResult[i]},{pacotesResult[i]},{_bytesResult[i]}\n'
    output.write(row)
