import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

def plotAll(dict_number_affiliates, dict_gender):
    figure1(dict_number_affiliates)
    figure2(dict_number_affiliates, dict_gender)
    figure3(dict_gender)
    figure4(dict_number_affiliates, dict_gender)
    figure5(dict_gender)
    figure6(dict_gender)
    figure7(dict_gender)
    return


def figure1(dict_number_affiliates):

    if dict_number_affiliates.get('PMDB') != None:
        del dict_number_affiliates['PMDB']
    tuple_affliliates = sorted(dict_number_affiliates.items(), key=itemgetter(1))
    party_list, number_affiliates = zip(*tuple_affliliates)

    plt.figure(figsize=(10, 15))
    y_pos = np.arange(len(party_list))
    plt.barh(y_pos, number_affiliates, align='center', alpha=0.7, color='red')
    plt.yticks(y_pos, party_list)
    plt.xlabel('Numero de Filiados')
    plt.title('Numero de Filiados por Partido Politico')
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_1.svg', dpi=1000)
    plt.close(plt.figure())
    return


def figure2(dict_number_affiliates, dict_gender):
    if dict_gender.get('PMDB') != None:
        del dict_gender['PMDB']
    norm_dict_gender={}
    for key, value in dict_gender.items():
        norm_dict_gender[key] = [value[0]/dict_number_affiliates[key],
                value[1]/dict_number_affiliates[key],
                1-(value[0]+value[1])/dict_number_affiliates[key]]
    tuple_gender = sorted(norm_dict_gender.items(), key=itemgetter(1))
    party_list, gender_array = zip(*tuple_gender)
    female, male, not_classified = zip(*gender_array)
    mean_female = np.mean(female)

    n_groups = len(party_list)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.7
    rects1 = plt.barh(index+bar_width, female, bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, male, bar_width, alpha=opacity, color='b', label='Homens')
    rects3 = plt.barh(index-bar_width, not_classified, bar_width, alpha=opacity, color='y', label='Nao Classificados')
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em Partidos Politicos')
    plt.yticks(index, party_list)
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_2.svg', dpi=1000)
    plt.close(plt.figure())
    return

def figure3(dict_gender):

    if dict_gender.get('PMDB') != None:
        del dict_gender['PMDB']
    norm_dict_gender={}
    for key, value in dict_gender.items():
        norm_dict_gender[key] = [-value[0]/(value[0]+value[1]), value[1]/(value[0]+value[1])]
    tuple_gender = sorted(norm_dict_gender.items(), key=itemgetter(1), reverse=True)
    party_list, gender_array = zip(*tuple_gender)
    female, male = zip(*gender_array)

    n_groups = len(party_list)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, female, bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, male, bar_width, alpha=opacity, color='b', label='Homens')
    rects3 = plt.axvline(x=0, color='k', linewidth=3.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em Partidos Politicos')
    plt.yticks(index, party_list)
    plt.xticks([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8])
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_3.svg', dpi=1000)
    plt.close(plt.figure())
    return


def figure4(dict_number_affiliates, dict_gender):
    if dict_gender.get('PMDB') != None:
        del dict_gender['PMDB']
    norm_dict_gender={}
    for key, value in dict_gender.items():
        norm_dict_gender[key] = [value[0]/dict_number_affiliates[key],
                value[1]/dict_number_affiliates[key],
                1-(value[0]+value[1])/dict_number_affiliates[key]]
    tuple_gender = sorted(norm_dict_gender.items(), key=itemgetter(1))
    party_list, gender_array = zip(*tuple_gender)
    female, male, not_classified = zip(*gender_array)
    mean_female = np.mean(female)
    male_female=[]
    for i in range(len(party_list)):
    	male_female.append(female[i] + male[i])

    n_groups = len(party_list)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, female, bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, male, bar_width, left=female, alpha=opacity, color='b', label='Homens')
    rects3 = plt.barh(index, not_classified, bar_width, left=male_female, alpha=opacity, color='y', label='Nao Classificados')
    rects4 = plt.axvline(x=0.5, color='k', label='Equidade de mulheres e homens', linestyle='--', linewidth=4.0)
    rects5 = plt.axvline(x=mean_female, color='g', label='Proporcao Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em Partidos Politicos')
    plt.yticks(index, party_list)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.legend(loc=1)
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_4.svg', dpi=1000)
    plt.close(plt.figure())
    return


def figure5(dict_gender):

    if dict_gender.get('PMDB') != None:
        del dict_gender['PMDB']
    norm_dict_gender={}
    for key, value in dict_gender.items():
        norm_dict_gender[key] = [value[0]/(value[0]+value[1]), value[1]/(value[0]+value[1])]
    tuple_gender = sorted(norm_dict_gender.items(), key=itemgetter(1))
    party_list, gender_array = zip(*tuple_gender)
    female, male = zip(*gender_array)
    mean_female = np.mean(female)

    n_groups = len(party_list)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, female, bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, male, bar_width, left=female, alpha=opacity, color='b', label='Homens')
    rects3 = plt.axvline(x=0.5, color='k', label='Equidade de mulheres e homens', linestyle='--', linewidth=4.0)
    rects4 = plt.axvline(x=mean_female, color='g', label='Proporcao Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em Partidos Politicos')
    plt.yticks(index, party_list)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_5.svg', dpi=1000)
    plt.close(plt.figure())
    return


def figure6(dict_gender):

    if dict_gender.get('PMDB') != None:
        del dict_gender['PMDB']
    norm_dict_gender={}
    for key, value in dict_gender.items():
        norm_dict_gender[key] = value[0]/(value[0]+value[1])
    tuple_gender = sorted(norm_dict_gender.items(), key=itemgetter(1))
    party_list, female = zip(*tuple_gender)
    mean_female = np.mean(female)

    n_groups = len(party_list)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    opacity = 0.7
    rects1 = plt.scatter(female, index, alpha=opacity, color='r', s=np.full(len(party_list),200))
    rects2 = plt.axvline(x=0.5, color='k', label='Equidade de mulheres e homens', linestyle='--', linewidth=4.0)
    rects3 = plt.axvline(x=mean_female, color='g', label='Proporcao Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em Partidos Politicos')
    plt.yticks(index, party_list)
    plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_6.svg', dpi=1000)
    plt.close(plt.figure())
    return


def figure7(dict_gender):

    if dict_gender.get('PMDB') != None:
        del dict_gender['PMDB']
    neg_dict_gender={}
    for key, value in dict_gender.items():
        neg_dict_gender[key] = [-value[0], value[1]]
    tuple_gender = sorted(neg_dict_gender.items(), key=itemgetter(1), reverse=True)
    party_list, gender_array = zip(*tuple_gender)
    female, male = zip(*gender_array)

    n_groups = len(party_list)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    rects1 = plt.barh(index, female, bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, male, bar_width, alpha=opacity, color='b', label='Homens')
    rects3 = plt.axvline(x=0, color='k', linewidth=3.0)
    plt.xlabel('Numero de Filiados')
    plt.ylabel('Partidos')
    plt.title('Numeros absolutos do genero em Partidos Politicos')
    plt.yticks(index, party_list)
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('img/Figure_7.svg', dpi=1000)
    plt.close(plt.figure())
    return

