import psycopg2
import secrets
import pandas as pd

PARTY_LIST = ['PPL', 'PMB', 'PSD', 'REDE', 'PODE', 'PSOL', 'PSDB', 'PROS', 'PHS', 'PRP', 'PSL', 'MDB', 'AVANTE', 'NOVO', 'PC DO B', 'PSB', 'PCO', 'PP', 'PSC', 'DC', 'PATRI', 'PR', 'PRB', 'PT', 'PDT', 'PTC', 'SD', 'PMN', 'PRTB', 'PV', 'PTB', 'PSTU', 'PCB', 'DEM', 'PPS']
STATE_LIST = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']


def create_df_party(number_affiliates, gender_party):
    df = pd.DataFrame.from_dict(gender_party, orient='index', columns=['female', 'male'])
    df['total'] = number_affiliates.values()
    df['not_class'] = df['total']-df['female']-df['male']
    return df

def create_df_state(gender_state):
    df = pd.DataFrame.from_dict(gender_state, orient='index', columns=['female', 'male'])
    return df

def make_proportions_clean(df):
    df2 = pd.DataFrame()
    df2['female'] = df['female']/(df['female']+df['male'])
    df2['male'] = df['male']/(df['female']+df['male'])
    return df2

def make_proportions(df):
    df2 = pd.DataFrame()
    df2['female'] = df['female']/df['total']
    df2['male'] = df['male']/df['total']
    df2['not_class'] = df['not_class']/df['total']
    return df2

def compute_number_affiliates():
    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    number_affiliates = dict.fromkeys(PARTY_LIST)
    for party in PARTY_LIST:
        cur.execute('''
                SELECT COUNT(numero_da_inscricao)
                FROM political_party
                WHERE sigla_do_partido = %s
                AND situacao_do_registro='REGULAR'; ''', [party])
        number_affiliates[party] = cur.fetchone()[0]
    conn.close()
    return number_affiliates

def compute_gender_party():
    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    gender_party = dict.fromkeys(PARTY_LIST)
    gender_classifications = ['F', 'M']
    for party in PARTY_LIST:
        print("Party", party, end=': ')
        temp=[]
        for gender in gender_classifications:
            cur.execute('''
                SELECT COUNT(political_party.primeiro_nome)
                FROM political_party
                INNER JOIN name_gender
                ON political_party.primeiro_nome = name_gender.first_name
                WHERE name_gender.classification= %s
                AND political_party.sigla_do_partido = %s
                AND political_party.situacao_do_registro='REGULAR'; ''', [gender,party])
            temp.append(cur.fetchone()[0])
        gender_party[party] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    conn.close()
    return gender_party

def compute_gender_state():
    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    gender_state = dict.fromkeys(STATE_LIST)
    gender_classifications = ['F', 'M']
    for state in STATE_LIST:
        print("State", state, end=': ')
        temp=[]
        for gender in gender_classifications:
            cur.execute('''
                SELECT COUNT(political_party.primeiro_nome)
                FROM political_party
                INNER JOIN name_gender
                ON political_party.primeiro_nome = name_gender.first_name
                WHERE name_gender.classification= %s
                AND political_party.uf = %s
                AND political_party.situacao_do_registro='REGULAR'; ''', [gender,state])
            temp.append(cur.fetchone()[0])
        gender_state[state] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    conn.close()
    return gender_state

def compute_candidates_gender():
    party_list = ['PPL', 'PMB', 'PSD', 'REDE', 'PODE', 'PSOL', 'SOLIDARIEDADE', 'PSDB', 'PROS', 'PHS', 'PRP', 'PSL', 'MDB', 'AVANTE', 'NOVO', 'PC do B', 'PSB', 'PCO', 'PP', 'PSC', 'DC', 'PATRI', 'PR', 'PRB', 'PT', 'PDT', 'PTC', 'PMN', 'PRTB', 'PV', 'PTB', 'PSTU', 'PCB', 'PPS', 'DEM']

    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    candidates_gender = dict.fromkeys(party_list)
    gender_classifications = ['FEMININO', 'MASCULINO']
    for party in party_list:
        print("Party", party, end=': ')
        temp=[]
        for gender in gender_classifications:
            cur.execute('''
                SELECT COUNT (DISTINCT nm_candidato)
                FROM candidates
                WHERE ds_genero = %s
                AND sg_partido = %s
                AND ds_situacao_candidatura = 'APTO'; ''', [gender,party])
            temp.append(cur.fetchone()[0])
        candidates_gender[party] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    candidates_gender['SD'] = candidates_gender.pop('SOLIDARIEDADE')
    candidates_gender['PC DO B'] = candidates_gender.pop('PC do B')
    conn.close()
    return candidates_gender

def compute_candidates_gender_state():
    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    candidates_gender = dict.fromkeys(STATE_LIST)
    gender_classifications = ['FEMININO', 'MASCULINO']
    for state in STATE_LIST:
        print("State", state, end=': ')
        temp=[]
        for gender in gender_classifications:
            cur.execute('''
                SELECT COUNT (DISTINCT nm_candidato)
                FROM candidates
                WHERE ds_genero = %s
                AND sg_uf= %s
                AND ds_situacao_candidatura = 'APTO'; ''', [gender,state])
            temp.append(cur.fetchone()[0])
        candidates_gender[state] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    conn.close()
    return candidates_gender

def compute_elected_gender_party():
    party_list = ['PPL', 'PMB', 'PSD', 'REDE', 'PODE', 'PSOL', 'SOLIDARIEDADE', 'PSDB', 'PROS', 'PHS', 'PRP', 'PSL', 'MDB', 'AVANTE', 'NOVO', 'PC do B', 'PSB', 'PCO', 'PP', 'PSC', 'DC', 'PATRI', 'PR', 'PRB', 'PT', 'PDT', 'PTC', 'PMN', 'PRTB', 'PV', 'PTB', 'PSTU', 'PCB', 'PPS', 'DEM']

    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    elected_gender_party = dict.fromkeys(party_list)
    gender_classifications = ['FEMININO', 'MASCULINO']
    for party in party_list:
        print("Party", party, end=': ')
        temp=[]
        for gender in gender_classifications:
            cur.execute('''
                SELECT COUNT (DISTINCT nm_candidato)
                FROM candidates
                WHERE ds_genero = %s
                AND sg_partido = %s
                AND ds_situacao_candidatura = 'APTO'
                AND cd_sit_tot_turno::INTEGER BETWEEN 1 AND 3; ''', [gender,party])
            temp.append(cur.fetchone()[0])
        elected_gender_party[party] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    elected_gender_party['SD'] = elected_gender_party.pop('SOLIDARIEDADE')
    elected_gender_party['PC DO B'] = elected_gender_party.pop('PC do B')
    conn.close()
    return elected_gender_party

def compute_elected_gender_state():
    conn = psycopg2.connect("dbname='scrappingtests' user=%s host='localhost' password=%s"%(secrets.user, secrets.psw))
    cur = conn.cursor()
    elected_gender = dict.fromkeys(STATE_LIST)
    gender_classifications = ['FEMININO', 'MASCULINO']
    for state in STATE_LIST:
        print("State", state, end=': ')
        temp=[]
        for gender in gender_classifications:
            cur.execute('''
                SELECT COUNT (DISTINCT nm_candidato)
                FROM candidates
                WHERE ds_genero = %s
                AND sg_uf= %s
                AND ds_situacao_candidatura = 'APTO'
                AND cd_sit_tot_turno::INTEGER BETWEEN 1 AND 3; ''', [gender,state])
            temp.append(cur.fetchone()[0])
        elected_gender[state] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    conn.close()
    return elected_gender
