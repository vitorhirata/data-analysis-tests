# Análise da Representatividade de Mulheres nas Eleições de 2018

## Informações sobre o projeto

Este projeto foi feito com a inteção de estudar ferramentas de programação e
análise de dados com dados reais e passando por toda o fluxo de coleta, análise
e apresentação dos resultados.

Neste estudo foi realizada uma análise da representatividade de mulheres nos partidos
estados brasileiros. Para tal foram utilizados dados de filiados a partidos
políticos, candidatos na eleição de 2018 e candidatos eleitos na eleição de 2018,
análisando a distribuição de mulheres por partido e por estado brasileiro.
[Neste arquivo](Representatividade_de_Mulheres_nos_Partidos_Politicos.pdf)
temos uma síntese dos principais resultados produzidos por esta análise.

## Fontes de Dados
Os dados sobre os filiados a partidos politicos foram retirados do TSE
(foram utilizados dados do final de 2018):
http://dados.gov.br/dataset/filiados-partidos-politicos


Os dados de gêneros de nomes vêm do IBGE e foram dispobilizados pela
plataforma brasil.io (este banco de dados foi utilizado pois no banco de dados
de filiados não havia o gênero das pessoas, assim com estes dados foi aferido
o gênero de cada pessoa filiada):
https://brasil.io/dataset/genero-nomes/nomes


Os dados de candidados e candidados eleitos em 2018 foram retirados do site do TSE:
http://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1/repositorio-de-dados-eleitorais

## Organização do repositório
O arquivo ['initialize-project.sh']('initialize-project.sh') inicializa o projeto, baixando todos os
conjuntos de dados mencionados acima e os colocando na pasta 'data'.

O arquivo ['set_database.py']('set_database.py') cria o banco de dados PostgreeSQL, sendo que este
arquivo utiliza um arquivo secrets.py que deve estar na raiz deste projeto.
Eventualmente podem existir dados errados no csv dos dados de filiados
a partidos políticos (por exemplo quando baixei o arquivo 'filiados_ptn_ac.csv'
possuia um erro na linha 1001) e eles precisam ser arrumados antes
de estruturar o banco de dados.

O arquivo ['analyse.py']('analyse.py)' é responsável por fazer as análises se utilizando
do banco de dados estruturado. Os resultados produzidos por este arquivo estão
na pasta 'clean-data', onde estão os csv's com os dados estruturados.

O arquivo ['plot.py']('plot.py') é responsável por produzir as imagens que estão na pasta
img e se utiliza dos csv's presentes na pasta clean-data.
