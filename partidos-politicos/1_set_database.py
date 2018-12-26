import psycopg2
from os import listdir
from secrets import psw

conn = psycopg2.connect("dbname='scrappingtests' user='vitor' host='localhost' password=%s"%(psw))
cur = conn.cursor()


# Create table political_party
cur.execute('''DROP TABLE political_party''')
cur.execute('''CREATE TABLE political_party
      (DATA_DA_EXTRACAO varchar,
 		HORA_DA_EXTRACAO varchar,
		NUMERO_DA_INSCRICAO varchar,
		NOME_DO_FILIADO varchar,
		SIGLA_DO_PARTIDO varchar,
		NOME_DO_PARTIDO varchar,
		UF varchar,
		CODIGO_DO_MUNICIPIO varchar,
		NOME_DO_MUNICIPIO varchar,
		ZONA_ELEITORAL varchar,
		SECAO_ELEITORAL varchar,
		DATA_DA_FILIACAO varchar,
		SITUACAO_DO_REGISTRO varchar,
		TIPO_DO_REGISTRO varchar,
		DATA_DO_PROCESSAMENTO varchar,
		DATA_DA_DESFILIACAO varchar,
		DATA_DO_CANCELAMENTO varchar,
		DATA_DA_REGULARIZACAO varchar,
		MOTIVO_DO_CANCELAMENTO varchar ); ''')

csvfiles = listdir("data/csv/")

for file in csvfiles:
	cur.execute('''COPY political_party FROM %s
		DELIMITER ';' CSV HEADER ENCODING 'ISO8859-14'; ''', ['/home/vitor/Code/scapping-tests/partidos-politicos/data/csv/'+file])

cur.execute('''
	ALTER TABLE political_party
	DROP COLUMN data_da_extracao,
	DROP COLUMN hora_da_extracao,
	DROP COLUMN codigo_do_municipio,
	DROP COLUMN zona_eleitoral,
	DROP COLUMN secao_eleitoral,
	DROP COLUMN motido_do_cancelamento;
''')

conn.commit()
conn.close()
