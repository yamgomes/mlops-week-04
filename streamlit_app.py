'''
Esse script prepara os dados usando pandas e
monta gráficos usando matplotlib para
visualizar mudanças na conversão do euro/real
Author: Yam
Dat-e: May 2022
'''
import logging
from matplotlib import style
import matplotlib.pyplot as plt
import pandas as pd
import streamlit

logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(message)s')

PATH_TO_FILE = './euro-daily-hist_1999_2022.csv'


def read_csv(path):
    '''
    Carrega os dados a partir do caminho até .csv

    Args:
        path: caminho para arquivo .csv

    Returns:
        dataframe: dados carregados no formato dataframe
    '''
    try:
        dataframe = pd.read_csv(path, sep=",", decimal=".")
        return dataframe
    except FileNotFoundError:
        logging.error('ERRO: arquivo %s não encontrado', path)
        return False


def test_read_csv(path):
    '''
    Testa o caminho até .csv

    Args:
        path: caminho para arquivo .csv

    Returns:
        assertion: se o caminho é válido
    '''
    return isinstance(path, str)


def plot(dataframe_entrada):
    '''
    Cria o gráfico a partir do dataframe

    Args:
        dataframe_entrada: dataframe a ser exibido

    '''
    dataframe_entrada = pd.read_csv(PATH_TO_FILE)

    dataframe_entrada.rename(columns={'[Brazilian real ]': 'Real',
                                      'Period\\Unit:': 'Tempo'},
                             inplace=True)
    dataframe_entrada['Tempo'] = pd.to_datetime(dataframe_entrada['Tempo'])
    dataframe_entrada.sort_values('Tempo', inplace=True)
    dataframe_entrada.reset_index(drop=True, inplace=True)
    dataframe = dataframe_entrada[['Tempo', 'Real']].copy()

    dataframe = dataframe[dataframe['Real'] != '-']
    dataframe['Real'] = dataframe['Real'].astype(float)

    dataframe['rolling_mean'] = dataframe['Real'].rolling(30).mean()

    style.use('fivethirtyeight')

    dataframe_lula = dataframe.copy()[(dataframe['Tempo'].dt.year >= 2003) & (
        dataframe['Tempo'].dt.year < 2011)]
    dataframe_dilma = dataframe.copy()[
        (dataframe['Tempo'].dt.year >= 2011) & (
            dataframe['Tempo'].dt.year < 2016)]
    dataframe_temer = dataframe.copy()[
        (dataframe['Tempo'].dt.year >= 2016) & (
            dataframe['Tempo'].dt.year < 2019)]
    dataframe_bolsonaro = dataframe.copy()[(
        dataframe['Tempo'].dt.year >= 2019)]

    plt.figure(figsize=(16, 8), dpi=400)
    ax1 = plt.subplot(2, 4, 1)
    ax2 = plt.subplot(2, 4, 2)
    ax3 = plt.subplot(2, 4, 3)
    ax4 = plt.subplot(2, 4, 4)
    ax5 = plt.subplot(2, 1, 2)
    axes = [ax1, ax2, ax3, ax4, ax5]

    for axis in axes:
        axis.set_ylim(0.8, 1.7)
        axis.set_yticks([1.0, 3.0, 5.0, 7.0])
        axis.set_yticklabels(['1', '3', '5', '7'],
                             alpha=0.5)
        axis.grid(alpha=0.5)

    ### Ax1: Lula
    ax1.plot(dataframe_lula['Tempo'], dataframe_lula['rolling_mean'],
             color='#FF3333')
    # ax1.set_xticks([2002, 2003, 2005,  2007,  2009,  2011, 2012])
    ax1.set_xticklabels(['', '2003', '',
                         '2005', '', '2007', '', '2009', '', '2011'],
                        alpha=0.5)

    ### Ax2: Dilma
    ax2.plot(dataframe_dilma['Tempo'], dataframe_dilma['rolling_mean'],
             color='#22dd22')
    ax2.set_xticklabels(['', '', '2012', '', '2014', '', '2016'],
                        alpha=0.5)

    ### Ax3: Temer
    ax3.plot(dataframe_temer['Tempo'], dataframe_temer['rolling_mean'],
             color='#593C8F')
    ax3.set_xticklabels(['2016', '', '', '2017', '', '', '2018', '', '', '2019'],
                        alpha=0.5)

    ### Ax4: Bolsonaro
    ax4.plot(dataframe_bolsonaro['Tempo'], dataframe_bolsonaro['rolling_mean'],
             color='#222222')
    ax4.set_xticklabels(['2019', '', '', '2020', '', '', '2021', '', '', '2022'],
                        alpha=0.5)

    ax5.plot(dataframe_lula['Tempo'], dataframe_lula['rolling_mean'],
             color='#FF3333')
    ax5.plot(dataframe_dilma['Tempo'], dataframe_dilma['rolling_mean'],
             color='#22dd22')
    ax5.plot(dataframe_temer['Tempo'], dataframe_temer['rolling_mean'],
             color='#593C8F')
    ax5.plot(dataframe_bolsonaro['Tempo'], dataframe_bolsonaro['rolling_mean'],
             color='#222222')
    ax5.grid(alpha=0.5)

    plt.text(12000, 17, 'Cotação do euro-real em relação ao mandato presidencial',
             fontsize=20, weight='bold',
             color='#000000')
    plt.text(12250, 15, 'LULA', fontsize=16, weight='bold',
             color='#FF3333')
    plt.text(14250, 15, 'DILMA', fontsize=16, weight='bold',
             color='#22dd22')
    plt.text(16250, 15, 'TEMER', fontsize=16, weight='bold',
             color='#593C8F')
    plt.text(18250, 15, 'BOLSONARO', fontsize=16, weight='bold',
             color='#222222')
    streamlit.pyplot(plt)


if __name__ == "__main__":
    df = read_csv(PATH_TO_FILE)
    plot(df)
