% openfig("../imagens/dados_originais/minuto1/intervalo_semana2/dia1/bytesps.fig");


for M = 1:5
    for S = 2:4
        for D = 1:7
            mkdir(strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D)))
%             IP de Origem
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f1 = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/iporigem.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,1), '--b');
            legend(legends, "Location", "southwest");
            saveas(f1, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/iporigem.jpg"));
            close()
            %             Porta de Origem
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f2 = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/portaorigem.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,2), '--b');
            legend(legends, "Location", "southwest");
            saveas(f2, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/portaorigem.jpg"));
            close()
            %             IP de Destino
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f3 = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/ipdestino.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,3), '--b');
            legend(legends, "Location", "southwest");
            saveas(f3, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/ipdestino.jpg"));
            close()
            %             Porta de Destino
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f4 = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/portadestino.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,4), '--b');
            legend(legends, "Location", "southwest");
            saveas(f4, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/portadestino.jpg"));
            close()
            %             Pacotes por Segundo
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f5 = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/pacotesps.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,5), '--b');
            legend(legends, "Location", "southwest");
            saveas(f5, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/pacotesps.jpg"));
            close()
            %             Bytes por Segundo
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f6 = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/bytesps.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,6), '--b');
            legend(legends, "Location", "southwest");
            saveas(f6, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/bytesps.jpg"));
            close()
        end
    end
end