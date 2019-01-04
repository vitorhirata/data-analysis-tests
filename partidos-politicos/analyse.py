import psycopg2
from secrets import psw

PARTY_LIST = ['PPL', 'PMB', 'PSD', 'REDE', 'PODE', 'PSOL', 'PSDC', 'PSDB', 'PROS', 'PHS', 'PRP', 'PSL', 'MDB', 'AVANTE', 'NOVO', 'PC DO B', 'PTN', 'PSB', 'PCO', 'PP', 'PSC', 'DC', 'PMDB', 'PATRI', 'PR', 'PRB', 'PT', 'PDT', 'PTC', 'SD', 'PMN', 'PRTB', 'PV', 'PTB', 'PSTU', 'PCB', 'DEM', 'PT DO B', 'PPS']

def compute_number_affiliates():
    conn = psycopg2.connect(" dbname='scrappingtests' user='vitor' host='localhost' password=%s"%(psw))
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

def compute_gender_count():
    conn = psycopg2.connect(" dbname='scrappingtests' user='vitor' host='localhost' password=%s"%(psw))
    cur = conn.cursor()
    gender_count = dict.fromkeys(PARTY_LIST)
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
        gender_count[party] = temp
        print("Mulheres =", temp[0], ", Homens =", temp[1])
    conn.close()
    return gender_count
