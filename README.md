# paper_HLPFK_2024
Repositório referente ao artigo "Otimização da associação entre estações base e equipamentos de usuário com auxílio de Aprendizado Federado para suporte a Realidade Aumentada Móvel" publicado no SBRC 2024

# Como citar
Caso o conteúdo auxilie em sua pesquisa considere citar o artigo: ?

# Sobre o conteúdo

## Aprendizado_Federado
1. Fed_Learning_SBRC_2024.ipynb - 
Script em Jupyter Notebook que implementa o sistema de Aprendizado Federado com redes neurais recorrentes utilizado no arquivo, permitindo o treinamento distribuído de modelos personalizados para cada usuário, em múltiplas estações base, com coordenação centralizada por um servidor.
Ao final do processamento os modelos otimizados de cada usuário são salvos assim como informações de normalização necessários para a utilização destes.
Adicionalmente, os conjuntos de dados que dão origem aos gráficos das figuras 2, 3 e 4 também são gerados por esse script.
2. 20_users_1_hour_sorted.csv - 
Dados de treinamento por usuário contemplando o identificador do usuário assim como informações de localização (x, y) e orientação (o).
3. SUMO_Script.py - 
Script para simulação de 20 usuários se deslocando ao longo do Campus Samambaia (UFG) durante 1 hora (3600 segundos).

## Graficos
Scripts em Jupyter Notebook para a geração dos gráficos quem envolvem as redes neurais recorrentes utilizadas na publicação (GRU, ESN, LSTM).

## Dados de Treinamento
Os dados de treinamento foram obtidos através da ferramenta de simulação de mobilidade urbana (SUMO).
O script para a criação do conjunto de dados está disponível no arquivo: SUMO_Script.py
