% openfig("../imagens/dados_originais/minuto1/intervalo_semana2/dia1/bytesps.fig");


for M = 1:5
    for S = 2:4
        for D = 1:7
            mkdir(strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D)))
            legends = {"Entropia na primeira semana", "Baseline", "Entropia do dia com anomalias"};
%             adicionando o baseline dos dias com anomalias aos gráficos
%             já existentes
            f = openfig(strcat("../imagens/dados_originais/minuto", num2str(M), "/intervalo_semana", num2str(S), "/dia", num2str(D), "/bytesps.fig"));
%             clf("reset");
            anomalies = csvread(strcat("../dados_anomalos/entropy/", num2str(M), "/", num2str(D), ".csv"), 1, 1);
            plot(1:size(anomalies, 1), anomalies(:,6), '--b');
%             legend(legends, "Location", "southwest");
            saveas(f, strcat("../imagens/dados_anomalos/minuto", num2str(M),"/intervalo_semana", num2str(S), "/dia", num2str(D), "/bytesps.jpg"));
        end
    end
end