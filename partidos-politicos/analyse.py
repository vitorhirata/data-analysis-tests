import psycopg2
import secrets
import pandas as pd

PARTY_LIST = ['PPL', 'PMB', 'PSD', 'REDE', 'PODE', 'PSOL', 'PSDC', 'PSDB', 'PROS', 'PHS', 'PRP', 'PSL', 'MDB', 'AVANTE', 'NOVO', 'PC DO B', 'PTN', 'PSB', 'PCO', 'PP', 'PSC', 'DC', 'PMDB', 'PATRI', 'PR', 'PRB', 'PT', 'PDT', 'PTC', 'SD', 'PMN', 'PRTB', 'PV', 'PTB', 'PSTU', 'PCB', 'DEM', 'PT DO B', 'PPS']
STATE_LIST = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']


def create_df_party(number_affiliates, gender_party):
    df = pd.DataFrame.from_dict(gender_party, orient='index', columns=['female', 'male'])
    df = df.drop(['PMDB'])
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
