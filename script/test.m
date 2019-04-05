% M1 = csvread("../dados_rede/data/entropy/1/1.csv",1,1);
% %Leitura dos demais arquivos (2 é o menor número para S)
% M2 = csvread("../dados_rede/data/entropy/1/8.csv",1,1);
% if S > 2
%      M3 = csvread("../dados_rede/data/entropy/1/15.csv",1,1);
% end
% if S > 3
%      M4 = csvread("../dados_rede/data/entropy/1/22.csv",1,1);
% end

% os intervalos de minutos
% for M = 1:5
%     % S = quantidade de semanas para se fazer os cálculos
%     for S = 2:4
%     % Os dias a serem lidos
%         for D = 1:7
%             disp(strcat("../dados_rede/data/entropy/", num2str(S), "/", num2str(D)))
%         end
%     end
% end1

M1 = csvread("../dados_rede/data/entropy/1/1.csv", 1, 1);
disp(size(M1, 1))
disp(size(M1, 2))