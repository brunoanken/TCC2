function [output] = pso(dados,omega,c1,c2,K,N)
%PSO A função PSO recebe o vetor de dados para o qual deseja-se calcular o Baseline e retorna como
%resposta o baseline de acordo com a distância euclidiana minimizada.
%   dados: vetor linha (1xS) onde S é o número de semanas
%   omega: coeficiente de inércia
%   c1: peso individual
%   c2: peso global
%   K: tamanho da população
%   N: número máximo de iterações

     %Número de semanas
     S = length(dados);

     %Matriz dos candidatos
     C = unifrnd(min(dados),max(dados),K,1);
     %Matriz dos melhores candidatos individuais
     C_local = C;
     %Vetor resultado da função custo para cada candidato
     F = zeros(K,1);
     
     for i=1:K
        F(i) = norm(C(i)-dados);
     end
     
     %Melhores funções individuais
     F_local = F;
     
     %Melhor global
     [F_best,idx] = min(F);
     C_best = C(idx);
     
     %Velocidade Inicial Aleatória
     V = randn(K,1);
     
     %Limite de iterações
     for i=1:N
     
          V = omega.*V + ... % Velocidade vezes inércia
               c1 .* unifrnd(0,1,K,1) .* (C - C_local) + ... %Contribuição individual
               c2 .* unifrnd(0,1,K,1) .* (C - C_best); % Contribuição global
          
          C = C + V; %Atualizando Posições
          
          %Verificando para cada indivíduo da população se houve melhora
          for k=1 : K
               
               F(k) = norm(C(k)-dados);
               
               %Comparando posição atual com a melhor do indivíduo
               if(F(k) < F_local(k))
                    F_local(k) = F(k);
                    C_local(k) = C(k);
               end
               
               %Comparando a posição atual com a melhor global
               if(F(k) < F_best)
                    F_best = F(k);
                    C_best = C(k);
               end
               
          end
                        
          
     end
     
     output = C_best;
          
end
