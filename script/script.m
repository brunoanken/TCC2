%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%    Script para cálculo do baseline de um dia da semana nas 6 dimensões analisadas
%    (entropias de ip de origem, porta de origem, ip de destino, porta de destino, pacotes
%    por segundo e bytes por segundo).
%
%    Autores: Lucas Dias Hiera Sampaio, Bruno Anken Moromizato Zaninello e Jhordan Garcia
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Conjuntos dos dias de mesmo tipo (segundas, terças, quartas etc.)
r1 = [1, 8, 15, 22];
r2 = [2, 9, 16, 23];
r3 = [3, 10, 17, 24];
r4 = [4, 11, 18, 25];
r5 = [5, 12, 19, 26];
r6 = [6, 13, 20, 27];
r7 = [7, 14, 21, 28];

% não vai até o 31 pois o intervalo é de 4 semanas no máximo

%Número de Semanas para montar o baseline
S = 4;

% Alterar a estrutura de leitura para ler por semanas, não apenas de maneira consecutiva (?)

%Leitura do arquivo para uma matriz 1440x6 (Para intervalos de 1 minuto)
%Para intervalos de 5 min a matriz será 288x6 e para 10 minutos 144x6
M1 = csvread("../dados_rede/data/entropy/1/1.csv",1,1);
%Leitura dos demais arquivos (2 é o menor número para S)
M2 = csvread("../dados_rede/data/entropy/1/8.csv",1,1);
if S > 2
     M3 = csvread("../dados_rede/data/entropy/1/15.csv",1,1);
end
if S > 3
     M4 = csvread("../dados_rede/data/entropy/1/22.csv",1,1);
end

%Transformando as matrizes de cada arquivo em uma única hipermatriz
% Todos os arquivos possuem o mesmo tamanho, tanto de colunas quanto de
% linhas, portanto é possível criar a matriz sem se preocupar com tamanhos
% dinâmicos dos arquivos
Dados = zeros(S,size(M1,1),size(M2,2));
for i=1:S
     
     if i == 1
          Dados(i,:,:) = M1;
     elseif i == 2
          Dados(i,:,:) = M2;
     elseif i == 3
          Dados(i,:,:) = M3;
     else
          Dados(i,:,:) = M4;
     end
     
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Rodando o PSO para cada instante de tempo e dimensão analizada
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Parâmetros do PSO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Inércia
omega = 1;
% Pesos Individuais
c1 = 1;
% Pesos Globais
c2 = 1;
% População
K = 100;
% Número máx de iterações
N = 1000;

% Output para Baseline %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Baseline = zeros(size(M1,1),6);

%Para cada instante de tempo
for t=1 : size(Dados,2)
     
     disp(t);
     
     %Para cada dimensão analisada
     for d=1 : size(Dados,3)
          
          temp = zeros(1,S);
          temp = transpose(Dados(:,t,d));
          
          Baseline(t,d) = pso(temp,omega,c1,c2,K,N);         
          
     end
     
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Plotando
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Plot 1 Entropia IP de Origem
figure(1);
plot(1:1440,Dados(1,:,1),'--r')
hold on
plot(1:1440,Dados(2,:,1),'--b')
if S > 2
     plot(1:1440,Dados(3,:,1),'--g')
end
if S > 3
     plot(1:1440,Dados(4,:,1),'--p')
end
plot(1:1440,Baseline(:,1),'-k')
saveas(gcf, '../imagens/dados_originais/1/iporigem.jpg')

% Plot 2 Entropia Porta de Origem
figure(2);
plot(1:1440,Dados(1,:,2),'--r')
hold on
plot(1:1440,Dados(2,:,2),'--b')
if S > 2
     plot(1:1440,Dados(3,:,2),'--g')
end
if S > 3
     plot(1:1440,Dados(4,:,2),'--p')
end
plot(1:1440,Baseline(:,2),'-k')
saveas(gcf, '../imagens/dados_originais/1/portaorigem.jpg')

% Plot 3 Entropia IP de Destino
figure(3)
plot(1:1440,Dados(1,:,3),'--r')
hold on
plot(1:1440,Dados(2,:,3),'--b')
if S > 2
     plot(1:1440,Dados(3,:,3),'--g')
end
if S > 3
     plot(1:1440,Dados(4,:,3),'--p')
end
plot(1:1440,Baseline(:,3),'-k')
saveas(gcf, '../imagens/dados_originais/1/portadestino.jpg')

% Plot 4 Entropia Porta de Destino
figure(4)
plot(1:1440,Dados(1,:,4),'--r')
hold on
plot(1:1440,Dados(2,:,4),'--b')
if S > 2
     plot(1:1440,Dados(3,:,4),'--g')
end
if S > 3
     plot(1:1440,Dados(4,:,4),'--p')
end
plot(1:1440,Baseline(:,4),'-k')
saveas(gcf, '../imagens/dados_originais/1/portadestino.jpg')

% Plot 5 Pacotes por Segundo
figure(5)
plot(1:1440,Dados(1,:,5),'--r')
hold on
plot(1:1440,Dados(2,:,5),'--b')
if S > 2
     plot(1:1440,Dados(3,:,5),'--g')
end
if S > 3
     plot(1:1440,Dados(4,:,5),'--p')
end
plot(1:1440,Baseline(:,5),'-k')
saveas(gcf, '../imagens/dados_originais/1/pacotesps.jpg')

% Plot 6 Bytes por Segundo
figure(6)
plot(1:1440,Dados(1,:,6),'--r')
hold on
plot(1:1440,Dados(2,:,6),'--b')
if S > 2
     plot(1:1440,Dados(3,:,6),'--g')
end
if S > 3
     plot(1:1440,Dados(4,:,6),'--p')
end
plot(1:1440,Baseline(:,6),'-k')
saveas(gcf, '../imagens/dados_originais/1/bytesps.jpg')
