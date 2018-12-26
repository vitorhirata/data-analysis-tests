import psycopg2
from secrets import psw

conn = psycopg2.connect("dbname='scrappingtests' user='vitor' host='localhost' password=%s"%(psw))
cur = conn.cursor()

party_list = ['PPL', 'PMB', 'PSD', 'REDE', 'PODE', 'PSOL', 'PSDC', 'PSDB', 'PROS', 'PHS', 'PRP', 'PSL', 'MDB', 'AVANTE', 'NOVO', 'PC DO B', 'PTN', 'PSB', 'PCO', 'PP', 'PSC', 'DC', 'PMDB', 'PATRI', 'PR', 'PRB', 'PT', 'PDT', 'PTC', 'SD', 'PMN', 'PRTB', 'PV', 'PTB', 'PSTU', 'PCB', 'DEM', 'PT DO B', 'PPS']
numero_filiados = []

for party in party_list:
    cur.execute('''
        SELECT COUNT(numero_da_inscricao) AS NumPeople
        FROM political_party
        WHERE sigla_do_partido = %s; ''', [party])
    numero_filiados.append(cur.fetchone()[0])


conn.commit()
conn.close()
