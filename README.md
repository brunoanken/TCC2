# Trabalho de Conclusão de Curso 2

Trabalho realizado como requisito parcial para a obtenção do grau de Bacharel em Engenharia de Computação.

Todos os arquivos dentro da pasta `script` foram desenvolvidos para atingir os objetivos deste trabalho.

## Requisitos
Cada arquivo Python deve ser executado pela linha de comando e chamado a partir da raíz do diretório ao qual pertence.

Para o arquivo `data_rw.py` é necessária a instalação da ferramente de linha de comando [nfdump](https://github.com/phaag/nfdump).

Para todos os outros arquivos Python é necessária a instalação da biblioteca [pandas](https://github.com/pandas-dev/pandas).

## Pasta `script`
### `data_rw.py`
Realiza a leitura dos arquivos no formato `nfcapd` e grava os dados extraídos em formato `csv`.

### `probability.py`
Realiza a leitura dos dados no formato `csv` gerados pelo script `data_rw.py` e calcula a entropia do IP de origem, porta de origem,
ip de destino, porta de destino e as médias de bytes por segundo e pacotes por segundo para intervalos de 1, 2, 3, 4 e 5 segundos.
Os resultados são gravados em novos arquivos no formato `csv`.

### `pso.m`
Script na linguagem MatLab que contém o algoritmo do PSO utilizado pelo script `script.m`.

### `script.m`
Realiza a leitura dos dados gerados pelo script `probability.py` e calcula o baseline para intervalos de 2, 3 e 4 semanas para cada 
um dos ntervalos de minutos para os quais as entropias e médias foram calculadas. Gráficos do baseline também são gerados.

### `script_anomaly.m`

Realiza a geração de gráficos contendo as entropias e as médias dos resultados da injeção de anomalias em cima dos gráficos gerados pelo
script `script.m`.

## Pasta `injection`

### `main.py`
Realiza a injeção de dados anômalos simulando ataques DoS ou DDoS dentro dos arquivos `csv` gerados pelo script `data_rw.py` e grava os
resultados em novos arquivos `csv`.

### `probability.py`
Executa a mesma função de `probability.py` da raíz da pasta `script`, porém para os dados gerados pelo script `main.py` da pasta 
`injection`.

## Pasta `conclusions`
### `errors.py`
Realiza o cálculo dos erros entre as entropias e médias de cada dia com medições da rede e seu baseline correspondente.
Salva os resultados no formato `xlsx`.

### `errors_anomalias.py`
Realiza o cálculo dos erros entre as entropias e médias dos dias com anomalias injetadas e seu baseline correspondente.
Salva os resultados no formato `xlsx`.

### `errors_conclusions.py`
Realiza o cálculo da média aritmética simples entre todos os dias para cada intervalo de semana e minutos a partir dos dados gerados
pelo script `errors.py` e imprime no console os menores resultados de cada dimensão no console.

### `errors_anomalies_conclusions.py`
Realiza o cálculo da média aritmética simples entre todos os dias para cada intervalo de semana e minutos a partir dos dados gerados
pelo script `errors_anomalies.py` e imprime no console os menores resultados de cada dimensão no console.

### `difference.py`
Realiza o cálculo da diferença de resultados entre o baseline para os 7 dias da semana no intervalo de horas escolhido na combinação
de intervalo de minutos e de semanas. Salva os resultados no formato `xlsx`.



