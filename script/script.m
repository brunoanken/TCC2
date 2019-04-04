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
% como são 7 dias na semana é só fazer um loop que itera do número 1 ao
% número 7
% r1 = [1, 8, 15, 22];
% r2 = [2, 9, 16, 23];
% r3 = [3, 10, 17, 24];
% r4 = [4, 11, 18, 25];
% r5 = [5, 12, 19, 26];
% r6 = [6, 13, 20, 27];
% r7 = [7, 14, 21, 28];

% não vai até o 31 pois o intervalo é de 4 semanas no máximo

% Os intervalos de minutos a serem percorridos
for M = 1:5
    disp(M)
    % Os intervalos de semanas a serem rodados
    for S = 2:4
        disp(S)
        % Loop para percorrer os dias da semana, 1 a 1, aplicando seus intervalos
        for D = 1:7
            disp(D)
            %Leitura do arquivo para uma matriz 1440x6 (Para intervalos de 1 minuto)
            %Para intervalos de 5 min a matriz será 288x6 e para 10 minutos 144x6
            M1 = csvread(strcat("../dados_rede/data/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);

            %Leitura dos demais arquivos (2 é o menor número para S)
            M2 = csvread(strcat("../dados_rede/data/entropy/", num2str(M), "/", num2str(D + 7), ".csv"), 1, 1);
            if S > 2
              M3 = csvread(strcat("../dados_rede/data/entropy/", num2str(M), "/", num2str(D + 14), ".csv"), 1, 1);
            end
            if S > 3
              M4 = csvread(strcat("../dados_rede/data/entropy/", num2str(M), "/", num2str(D + 21), ".csv"), 1, 1);
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

%                  disp(t);

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
            % cria a pasta de destino dos dados
            mkdir(strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D)))
            % Plot 1 Entropia IP de Origem
            f1 = figure(1);
            plot(1:1440,Dados(1,:,1),'--r')
            hold on
            plot(1:1440,Dados(2,:,1),'--b')
            if S > 2
                 plot(1:1440,Dados(3,:,1),'--g')
            end
            if S > 3
                 plot(1:1440,Dados(4,:,1),'--p')
            end
            plot(1:1440,Baseline(:,1),'-k');          
            saveas(f1, strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/iporigem.jpg"))

            % Plot 2 Entropia Porta de Origem
            f2 = figure(2);
            plot(1:1440,Dados(1,:,2),'--r')
            hold on
            plot(1:1440,Dados(2,:,2),'--b')
            if S > 2
                 plot(1:1440,Dados(3,:,2),'--g')
            end
            if S > 3
                 plot(1:1440,Dados(4,:,2),'--p')
            end
            plot(1:1440,Baseline(:,2),'-k');
            saveas(f2, strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/portaorigem.jpg"))

            % Plot 3 Entropia IP de Destino
            f3 = figure(3);
            plot(1:1440,Dados(1,:,3),'--r')
            hold on
            plot(1:1440,Dados(2,:,3),'--b')
            if S > 2
                 plot(1:1440,Dados(3,:,3),'--g')
            end
            if S > 3
                 plot(1:1440,Dados(4,:,3),'--p')
            end
            plot(1:1440,Baseline(:,3),'-k');
            saveas(f3, strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/ipdestino.jpg"))

            % Plot 4 Entropia Porta de Destino
            f4 = figure(4);
            plot(1:1440,Dados(1,:,4),'--r')
            hold on
            plot(1:1440,Dados(2,:,4),'--b')
            if S > 2
                 plot(1:1440,Dados(3,:,4),'--g')
            end
            if S > 3
                 plot(1:1440,Dados(4,:,4),'--p')
            end
            plot(1:1440,Baseline(:,4),'-k');
            saveas(f4, strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/portadestino.jpg"))

            % Plot 5 Pacotes por Segundo
            f5 = figure(5);
            plot(1:1440,Dados(1,:,5),'--r')
            hold on
            plot(1:1440,Dados(2,:,5),'--b')
            if S > 2
                 plot(1:1440,Dados(3,:,5),'--g')
            end
            if S > 3
                 plot(1:1440,Dados(4,:,5),'--p')
            end
            plot(1:1440,Baseline(:,5),'-k');
            saveas(f5, strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/pacotesps.jpg"))

            % Plot 6 Bytes por Segundo
            f6 = figure(6);
            plot(1:1440,Dados(1,:,6),'--r')
            hold on
            plot(1:1440,Dados(2,:,6),'--b')
            if S > 2
                 plot(1:1440,Dados(3,:,6),'--g')
            end
            if S > 3
                 plot(1:1440,Dados(4,:,6),'--p')
            end
            plot(1:1440,Baseline(:,6),'-k');
            saveas(f6, strcat("../imagens/dados_originais/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/bytesps.jpg"))
        end
    end
end