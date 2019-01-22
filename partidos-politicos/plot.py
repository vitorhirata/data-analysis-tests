import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import geopandas as gpd
import pandas as pd
import analyse

def plotAll(df, df2, df3, df4, df5, df6):
    plot_num_affiliates(df)
    plot_gender_abs(df)
    plot_gender_relative_bar_full(df)
    plot_gender_relative_bar_cut(df, 'Filiados a Partidos Politicos', '4_gender_relative_bar_cut')
    plot_gender_relative_line(df, 'Filiados a Partidos Politicos', '5_gender_relative_line')
    plot_gender_map(df2, 'Filiadas por Estado', '6_gender_map')
    plot_gender_relative_bar_cut(df3, 'Candidatos a Eleicao', '7_candidates_gender_relative_bar_cut')
    plot_gender_relative_line(df3, 'Candidatos a Eleicao', '8_candidates_relative_line')
    plot_gender_map(df4, 'Candidatas por Estado', '9_candidates_gender_map')
    plot_gender_relative_bar_cut(df5, 'Candidatos Eleitos', '10_elected_gender_relative_bar_cut')
    plot_gender_relative_line(df5, 'Candidatos Eleitos', '11_elected_relative_line')
    plot_gender_map(df6, 'Eleitas por Estado', '12_elected_gender_map')
    return


def plot_num_affiliates(df):
    df2 = df.sort_values('total')

    plt.figure(figsize=(10, 15))
    y_pos = np.arange(len(df))
    plt.barh(y_pos, df2['total'], align='center', alpha=0.7, color='red')
    plt.yticks(y_pos, df2.index)
    plt.xlabel('Numero de Filiados')
    plt.title('Numero de Filiados por Partido Politico')
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/1_num_affiliates.svg', dpi=1000)
    plt.close(plt.figure())
    return

def plot_gender_abs(df):
    df2 = df.sort_values('total')
    df2['female'] = - df2['female']

    n_groups = len(df2)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    rects1 = plt.barh(index, df2['female'], bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, df2['male'], bar_width, alpha=opacity, color='b', label='Homens')
    rects3 = plt.axvline(x=0, color='k', linewidth=3.0)
    plt.xlabel('Numero de Filiados')
    plt.ylabel('Partidos')
    plt.title('Numeros absolutos do genero em Filiados a Partidos Politicos')
    plt.yticks(index, df2.index)
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/2_gender_abs.svg', dpi=1000)
    plt.close(plt.figure())
    return


def plot_gender_relative_bar_full(df):
    df2 = analyse.make_proportions(df)
    df2 = df2.sort_values('female')

    n_groups = len(df)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, df2['female'], bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, df2['male'], bar_width, left=df2['female'], alpha=opacity, color='b', label='Homens')
    rects3 = plt.barh(index, df2['not_class'], bar_width, left=df2['female']+df2['male'], alpha=opacity, color='y', label='Nao Classificados')
    rects4 = plt.axvline(x=0.5, color='k', label='Equidade de mulheres e homens', linestyle='--', linewidth=4.0)
    rects5 = plt.axvline(x=df2['female'].mean(), color='g', label='Proporcao Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em Filiados a Partidos Politicos')
    plt.yticks(index, df2.index)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.legend(loc=1)
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/3_gender_relative_bar_full.svg', dpi=1000)
    plt.close(plt.figure())
    return


def plot_gender_relative_bar_cut(df, str1, str2):
    df2 = analyse.make_proportions_clean(df)
    df2 = df2.sort_values('female')
    df2.dropna(subset=['female'], inplace=True)

    n_groups = len(df2)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.7
    rects1 = plt.barh(index, df2['female'], bar_width, alpha=opacity, color='r', label='Mulheres')
    rects2 = plt.barh(index, df2['male'], bar_width, left=df2['female'], alpha=opacity, color='b', label='Homens')
    rects3 = plt.axvline(x=0.5, color='k', label='Equidade de mulheres e homens', linestyle='--', linewidth=4.0)
    rects4 = plt.axvline(x=df2['female'].mean(), color='g', label='Proporcao Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de Genero em ' + str1)
    plt.yticks(index, df2.index)
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.legend()
    plt.tight_layout()
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.savefig('test_figure/'+str2+'.svg', dpi=1000)
    plt.close(plt.figure())
    return


def plot_gender_relative_line(df, str1, str2):
    df2 = analyse.make_proportions_clean(df)
    df2 = df2.sort_values('female')
    df2.dropna(subset=['female'], inplace=True)

    n_groups = len(df2)
    fig, ax = plt.subplots(figsize=(10, 15))
    index = np.arange(n_groups)
    opacity = 0.7
    rects1 = plt.scatter(df2['female'], index, alpha=opacity, color='r', s=np.full(len(df2),200))
    rects2 = plt.axvline(x=0.5, color='k', label='Equidade de mulheres e homens', linestyle='--', linewidth=4.0)
    rects3 = plt.axvline(x=df2['female'].mean(), color='g', label='Proporcao Media de Mulheres', linewidth=2.0)
    plt.xlabel('Proporcao')
    plt.ylabel('Partidos')
    plt.title('Proporcao de genero em ' + str1)
    plt.yticks(index, df2.index)
    plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    plt.legend()
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
    vmin, vmax = 0.05, 0.55

    gdf.plot(column='female', cmap = 'gnuplot2', legend=True, edgecolor = 'black', vmin=vmin, vmax=vmax, figsize=(15, 9))
    plt.xticks([])
    plt.yticks([])
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.title('Proporcao de Mulheres '+str1, fontsize=20)
    plt.tight_layout()
    plt.savefig('test_figure/'+str2+'.svg', dpi=1000)
    plt.close(plt.figure())
    return
