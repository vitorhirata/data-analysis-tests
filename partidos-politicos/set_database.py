import psycopg2
from os import listdir
from secrets import psw

conn = psycopg2.connect("dbname='scrappingtests' user='vitor' host='localhost' password=%s"%(psw))
cur = conn.cursor()

print("Creating table political_party")
# Create table political_party
cur.execute('''DROP TABLE political_party;  ''')
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
	cur.execute('''
            COPY political_party FROM %s
	    DELIMITER ';' CSV HEADER ENCODING 'ISO8859-14'; ''',
            ['/home/vitor/Code/scrapping-tests/partidos-politicos/data/csv/'+file])

cur.execute('''
	ALTER TABLE political_party
	DROP COLUMN data_da_extracao,
	DROP COLUMN hora_da_extracao,
	DROP COLUMN codigo_do_municipio,
	DROP COLUMN zona_eleitoral,
	DROP COLUMN secao_eleitoral,
	DROP COLUMN motivo_do_cancelamento;
''')

cur.execute('''ALTER TABLE political_party ADD COLUMN primeiro_nome varchar; ''')
#cur.execute('''CREATE EXTENSION unaccent; ''')
cur.execute('''UPDATE political_party SET primeiro_nome=unaccent(split_part(nome_do_filiado, ' ', 1)); ''')
print("Finish political_party creation.")



print("Creating table name_gender")
# Create table name_gender
cur.execute('''DROP TABLE name_gender''')
cur.execute('''CREATE TABLE name_gender
	(first_name varchar,
	group_name varchar,
	classification CHAR(1),
	frequency_female FLOAT,
	frequency_male INT,
	frequency_total INT,
	frequency_group BIGINT,
	ratio FLOAT,
	alternative_names varchar); ''')

cur.execute('''COPY name_gender FROM '/home/vitor/Code/scrapping-tests/partidos-politicos/data/names_gender.csv' DELIMITER ',' CSV HEADER; ''')

cur.execute('''
    ALTER TABLE name_gender
	DROP COLUMN frequency_female,
	DROP COLUMN frequency_male,
	DROP COLUMN frequency_total,
	DROP COLUMN frequency_group; ''')
print("Finish name_gender creation.")

conn.commit()
conn.close()