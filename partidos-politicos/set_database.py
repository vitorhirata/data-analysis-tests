import psycopg2
import secrets
from os import listdir

def create_political_party():

    print("Creating table political_party")

    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()

    # If the table already exist drop it
    try:
        cur.execute('''DROP TABLE political_party;  ''')
    except:
        pass

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

    csvfiles = listdir("data/affiliates/csv/")

    for file_name in csvfiles:
        file = open('data/affiliates/csv/'+file_name, 'r', encoding = 'ISO8859-14')
        cur.copy_expert('''COPY political_party FROM STDIN DELIMITER ';' CSV HEADER ENCODING 'ISO8859-14'; ''',file)

    cur.execute('''
        ALTER TABLE political_party
        DROP COLUMN data_da_extracao,
        DROP COLUMN hora_da_extracao,
        DROP COLUMN codigo_do_municipio,
        DROP COLUMN zona_eleitoral,
        DROP COLUMN secao_eleitoral,
        DROP COLUMN motivo_do_cancelamento;''')

    # If the extension unaccent does not exist create it
    try:
        cur.execute('''CREATE EXTENSION unaccent; ''')
    except:
        pass

    cur.execute('''ALTER TABLE political_party ADD COLUMN primeiro_nome varchar; ''')
    cur.execute('''UPDATE political_party SET primeiro_nome=unaccent(split_part(nome_do_filiado, ' ', 1)); ''')
    print("Finish political_party creation.")

    conn.commit()
    conn.close()
    return

def create_name_gender():

    print("Creating table name_gender")
    # Create table name_gender

    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()


    # If the table already exist drop it
    try:
        cur.execute('''DROP TABLE name_gender; ''')
    except:
        pass

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

    file = open('data/names_gender.csv', 'r')
    cur.copy_expert('''COPY name_gender FROM STDIN DELIMITER ',' CSV HEADER; ''', file)

    cur.execute('''
        ALTER TABLE name_gender
    	DROP COLUMN frequency_female,
    	DROP COLUMN frequency_male,
    	DROP COLUMN frequency_total,
    	DROP COLUMN frequency_group; ''')
    print("Finish name_gender creation.")

    conn.commit()
    conn.close()
    return


def create_candidates():

    print("Creating table candidates")
    # Create table name_gender

    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()


    # If the table already exist drop it
    try:
        cur.execute('''DROP TABLE candidates; ''')
    except:
        pass

    cur.execute('''CREATE TABLE candidates
        (DT_GERACAO varchar,
        HH_GERACAO varchar,
        ANO_ELEICAO varchar,
        CD_TIPO_ELEICAO varchar,
        NM_TIPO_ELEICAO varchar,
        NR_TURNO varchar,
        CD_ELEICAO varchar,
        DS_ELEICAO varchar,
        DT_ELEICAO varchar,
        TP_ABRANGENCIA varchar,
        SG_UF varchar,
        SG_UE varchar,
        NM_UE varchar,
        CD_CARGO varchar,
        DS_CARGO varchar,
        SQ_CANDIDATO varchar,
        NR_CANDIDATO varchar,
        NM_CANDIDATO varchar,
        NM_URNA_CANDIDATO varchar,
        NM_SOCIAL_CANDIDATO varchar,
        NR_CPF_CANDIDATO varchar,
        NM_EMAIL varchar,
        CD_SITUACAO_CANDIDATURA varchar,
        DS_SITUACAO_CANDIDATURA varchar,
        CD_DETALHE_SITUACAO_CAND varchar,
        DS_DETALHE_SITUACAO_CAND varchar,
        TP_AGREMIACAO varchar,
        NR_PARTIDO varchar,
        SG_PARTIDO varchar,
        NM_PARTIDO varchar,
        SQ_COLIGACAO varchar,
        NM_COLIGACAO varchar,
        DS_COMPOSICAO_COLIGACAO varchar,
        CD_NACIONALIDADE varchar,
        DS_NACIONALIDADE varchar,
        SG_UF_NASCIMENTO varchar,
        CD_MUNICIPIO_NASCIMENTO varchar,
        NM_MUNICIPIO_NASCIMENTO varchar,
        DT_NASCIMENTO varchar,
        NR_IDADE_DATA_POSSE varchar,
        NR_TITULO_ELEITORAL_CANDIDATO varchar,
        CD_GENERO varchar,
        DS_GENERO varchar,
        CD_GRAU_INSTRUCAO varchar,
        DS_GRAU_INSTRUCAO varchar,
        CD_ESTADO_CIVIL varchar,
        DS_ESTADO_CIVIL varchar,
        CD_COR_RACA varchar,
        DS_COR_RACA varchar,
        CD_OCUPACAO varchar,
        DS_OCUPACAO varchar,
        NR_DESPESA_MAX_CAMPANHA varchar,
        CD_SIT_TOT_TURNO varchar,
        DS_SIT_TOT_TURNO varchar,
        ST_REELEICAO varchar,
        ST_DECLARAR_BENS varchar,
        NR_PROTOCOLO_CANDIDATURA varchar,
        NR_PROCESSO varchar); ''')

    file = open('data/candidates/consulta_cand_2018_BRASIL.csv', 'r', encoding = 'ISO8859-14')
    cur.copy_expert('''COPY candidates FROM STDIN DELIMITER ';' CSV HEADER ENCODING 'ISO8859-14'; ''',file)

    cur.execute('''
        ALTER TABLE candidates
        DROP COLUMN CD_TIPO_ELEICAO,
        DROP COLUMN NM_TIPO_ELEICAO,
        DROP COLUMN CD_ELEICAO,
        DROP COLUMN DS_ELEICAO,
        DROP COLUMN DT_ELEICAO,
        DROP COLUMN TP_ABRANGENCIA,
        DROP COLUMN SG_UE,
        DROP COLUMN NM_UE,
        DROP COLUMN SQ_CANDIDATO,
        DROP COLUMN NR_CANDIDATO,
        DROP COLUMN NR_CPF_CANDIDATO,
        DROP COLUMN NM_EMAIL,
        DROP COLUMN CD_SITUACAO_CANDIDATURA,
        DROP COLUMN CD_DETALHE_SITUACAO_CAND,
        DROP COLUMN DS_DETALHE_SITUACAO_CAND,
        DROP COLUMN TP_AGREMIACAO,
        DROP COLUMN NR_PARTIDO,
        DROP COLUMN SQ_COLIGACAO,
        DROP COLUMN NM_COLIGACAO,
        DROP COLUMN DS_COMPOSICAO_COLIGACAO,
        DROP COLUMN CD_NACIONALIDADE,
        DROP COLUMN DS_NACIONALIDADE,
        DROP COLUMN SG_UF_NASCIMENTO,
        DROP COLUMN CD_MUNICIPIO_NASCIMENTO,
        DROP COLUMN NM_MUNICIPIO_NASCIMENTO,
        DROP COLUMN DT_NASCIMENTO,
        DROP COLUMN NR_IDADE_DATA_POSSE,
        DROP COLUMN NR_TITULO_ELEITORAL_CANDIDATO,
        DROP COLUMN CD_GRAU_INSTRUCAO,
        DROP COLUMN DS_GRAU_INSTRUCAO,
        DROP COLUMN CD_ESTADO_CIVIL,
        DROP COLUMN DS_ESTADO_CIVIL,
        DROP COLUMN CD_OCUPACAO,
        DROP COLUMN DS_OCUPACAO,
        DROP COLUMN NR_DESPESA_MAX_CAMPANHA,
        DROP COLUMN ST_DECLARAR_BENS,
        DROP COLUMN NR_PROTOCOLO_CANDIDATURA,
        DROP COLUMN NR_PROCESSO; ''')
    print("Finish candidates creation.")

    conn.commit()
    conn.close()
    return

def create_all_tables():
    create_political_party()
    create_name_gender()
    create_candidates()
    create_candidates_elected()
    return
