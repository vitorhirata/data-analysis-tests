import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import geopandas as gpd
import pandas as pd
import analyse

def plotAll(dfFilliateParty, dfFilliateState, dfCandidateParty,
        dfCandidateState, dfElectedParty, dfElectedState):

    plot_num_affiliates(dfFilliateParty)
    plot_gender_abs(dfFilliateParty)
    plot_gender_relative_bar_full(dfFilliateParty)
    plot_gender_relative_bar_cut(dfFilliateParty, 'Filiados a Partidos Politicos',
            '4_gender_relative_bar_cut')
    plot_gender_relative_line(dfFilliateParty, 'Filiadas por Partido Político',
            '5_gender_relative_line')
    plot_gender_map(dfFilliateState, 'Filiadas por Estado', '6_gender_map')
    plot_gender_relative_bar_cut(dfCandidateParty, 'Candidatos à Eleição de 2018',
            '7_candidates_gender_relative_bar_cut')
    plot_gender_relative_line(dfCandidateParty, 'Candidatas à Eleição de 2018 por Partido Político',
            '8_candidates_relative_line')
    plot_gender_map(dfCandidateState, 'Candidatas\nem 2018 por Estado', '9_candidates_gender_map')
    plot_gender_relative_bar_cut(dfElectedParty, 'Candidatos Eleitos em 2018',
            '10_elected_gender_relative_bar_cut')
    plot_gender_relative_line(dfElectedParty, 'Eleitas em 2018 por Partido Político',
            '11_elected_relative_line')
    plot_gender_map(dfElectedState, 'Eleitas\nem 2018 por Estado', '12_elected_gender_map')
    return


def plot_num_affiliates(df):
    dfFix = df.sort_values('Total')

    plt.figure(figsize=(5, 10))
    y_pos = np.arange(len(df))
    plt.barh(y_pos, dfFix['Total'], align='center', alpha=0.7, color='red')
    plt.yticks(y_pos, dfFix.index)
    plt.xlabel('Numero de Filiados\n', fontsize=12)
    plt.gca().xaxis.tick_top()
    plt.gca().xaxis.set_label_position("top")
    plt.title('Numero de Filiados por Partido Politico\n', fontsize=15)
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.savefig('test_figure/1_num_affiliates.svg', dpi=1000)
    plt.close(plt.figure())
    return

def plot_gender_abs(df):
    dfFix = df.sort_values('Total')
    dfFix['Female'] = - dfFix['Female']

    n_groups = len(dfFix)
    fig, ax = plt.subplots(figsize=(7, 9))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    rects1 = plt.barh(index, dfFix['Female'], bar_width, alpha=opacity,
            color='r', label='Mulheres')
    rects2 = plt.barh(index, dfFix['Male'], bar_width, alpha=opacity,
            color='b', label='Homens')
    rects3 = plt.axvline(x=0, color='k', linewidth=3.0)
    plt.xlabel('Número de Filiados')
    plt.ylabel('Partido')
    plt.title('Números Absolutos de Filiados a Partidos Politicos por Gênero',
            fontsize=15)
    plt.yticks(index, dfFix.index)
    plt.xticks([-1000000, -500000, 0, 500000, 1000000],
            [1000000, 500000, 0, 500000, 1000000])
    plt.legend(loc='center right')
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/2_gender_abs.svg', dpi=1000)
    plt.close(plt.figure())
    return


def plot_gender_relative_bar_full(df):
    dfFix = analyse.make_proportions(df)
    dfFix = dfFix.sort_values('Female')

    n_groups = len(df)
    fig, ax = plt.subplots(figsize=(5, 9))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, dfFix['Female'], bar_width, alpha=opacity,
            color='r', label='Mulheres')
    rects2 = plt.barh(index, dfFix['Male'], bar_width, left=dfFix['Female'],
            color='b', alpha=opacity, label='Homens')
    rects3 = plt.barh(index, dfFix['Not_classified'], bar_width,
            left=dfFix['Female']+dfFix['Male'], alpha=opacity,
            color='y', label='Nao Classificados')
    rects4 = plt.axvline(x=0.5, color='k', linewidth=4.0,
            label='Equidade de mulheres e homens', linestyle='--')
    rects5 = plt.axvline(x=dfFix['Female'].mean(), color='g',
            label='Proporção Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporção')
    plt.ylabel('Partidos')
    plt.title('Proporção de Gênero em Filiados a Partidos Politicos')
    plt.yticks(index, dfFix.index)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.legend(loc=1)
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/3_gender_relative_bar_full.svg', dpi=1000)
    plt.close(plt.figure())
    return


def plot_gender_relative_bar_cut(df, str1, str2):
    dfFix = analyse.make_proportions_clean(df)
    dfFix = dfFix.sort_values('Female')
    dfFix.dropna(subset=['Female'], inplace=True)

    n_groups = len(dfFix)
    fig, ax = plt.subplots(figsize=(5, 9))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, dfFix['Female'], bar_width, alpha=opacity,
            color='r', label='Mulheres')
    rects2 = plt.barh(index, dfFix['Male'], bar_width, left=dfFix['Female'],
            color='b', alpha=opacity, label='Homens')
    rects3 = plt.axvline(x=0.5, color='k',
            label='Equidade de\nmulheres e homens', linestyle='--',
            linewidth=4.0)
    rects4 = plt.axvline(x=dfFix['Female'].mean(), color='g',
            label='Proporção Média\nde Mulheres', linewidth=2.0)
    plt.xlabel('Proporção')
    plt.ylabel('Partidos')
    plt.title('Proporção de Gênero em\n' + str1, fontsize=15)
    plt.yticks(index, dfFix.index)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/'+str2+'.svg', dpi=1000)
    plt.close(plt.figure())
    return


def plot_gender_relative_line(df, str1, str2):
    dfFix = analyse.make_proportions_clean(df)
    dfFix = dfFix.sort_values('Female')
    dfFix.dropna(subset=['Female'], inplace=True)

    n_groups = len(dfFix)
    fig, ax = plt.subplots(figsize=(6, 9))
    index = np.arange(n_groups)
    opacity = 0.7
    rects1 = plt.scatter(dfFix['Female'], index, alpha=opacity,
            color='r', s=np.full(len(dfFix),70))
    rects2 = plt.axvline(x=0.5, color='k', linewidth=4.0,
            label='Equidade de\nmulheres e homens', linestyle='--')
    rects3 = plt.axvline(x=dfFix['Female'].mean(), color='g',
            label='Proporção Média\nde Mulheres', linewidth=2.0)
    plt.xlabel('Proporção')
    plt.ylabel('Partidos')
    plt.title('Proporção de Mulheres\n' + str1, fontsize=15)
    plt.yticks(index, dfFix.index)
    plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    plt.legend(loc='center right')
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/'+str2+'.svg', dpi=1000)
    plt.close(plt.figure())
    return

def plot_gender_map(df, str1, str2):
    df = analyse.make_proportions_clean(df)
    gdf = gpd.read_file('data/br-states/estados.shp')
    gdf = gdf.merge(df, left_on='sigla', right_index=True, how='inner')
    vmin, vmax = gdf.Female.min() - 0.02, gdf.Female.max() + 0.02

    gdf.plot(column='Female', cmap = 'hot_r', legend=True,
            edgecolor = 'black', vmin=vmin, vmax=vmax, figsize=(7, 4))
    plt.xticks([])
    plt.yticks([])
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.title('Proporção de Mulheres '+str1, fontsize=15)
    plt.tight_layout()
    plt.savefig('test_figure/'+str2+'.svg', dpi=1000)
    plt.close(plt.figure())
    return
