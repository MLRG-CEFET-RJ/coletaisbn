# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 18:27:10 2019

@author: Daniel Favoreto & Eduardo Bezerra
"""

import pandas as pd
import numpy as np
import re
import argparse
import os
import json
from json2xml import json2xml
import sys
import isbnlib as il
import time
import collections

JSON_ACERVO_UNIFICADO = 'data/acervo_unificado.json'
COLUNAS_ACERVO_UNIFICADO = ['isbn13','titulo','assuntos','autores','idioma','editora','qtd_paginas', 'edicao']

def imprimir_primeiras_linhas(file_name):
    extensao_arquivo = re.search('\.(.*)', file_name).group()
    if(extensao_arquivo =='.csv'):
        df = pd.read_csv(file_name,dtype=str)
        print(df.head())
    else:
        df = pd.read_excel(file_name)
        print(df.head())
        
def imprimir_esquema(file_name):
    extensao_arquivo = re.search('\.(.*)', file_name).group()
    if extensao_arquivo =='.csv':
        print(pd.read_csv(file_name,nrows=1).columns)
    elif extensao_arquivo =='.xlsx':
        print(pd.read_excel(file_name,nrows=1).columns)

def importar_acervo_bibliotecario(args, input_file, col_isbn, cols_fonte, cols_destino):

    cols_fonte = cols_fonte.split(',')
    cols_destino = cols_destino.split(',')
    
    if os.path.isfile(JSON_ACERVO_UNIFICADO):
        df_unificado = pd.read_json(JSON_ACERVO_UNIFICADO, dtype=str)
    else:
        df_unificado = pd.DataFrame(columns=COLUNAS_ACERVO_UNIFICADO)

    df = pd.DataFrame()
    extensao_arquivo = re.search('\.(.*)', input_file).group()

    if extensao_arquivo == '.csv':
        df = pd.read_csv(input_file, dtype=str)
        df = df[cols_fonte]
    elif extensao_arquivo == '.xlsx':
        df = pd.read_excel(input_file, dtype=str)
        df = df[cols_fonte]
    else:
        print("ERRO: Arquivo a ser importado deve estar em formato CSV ou XLSX.")
        return

    if len(cols_fonte) != len(cols_destino):
        print("ERRO: listas de colunas fonte e destino devem ter mesmo tamanho.")
        return
    elif len(cols_fonte) == 0:
        print("ERRO: listas de colunas fonte e destino devem ter ser não vazias.")
        return

    # verifica se colunas existem no esquema unificado.
    for col in cols_destino:
        if col not in COLUNAS_ACERVO_UNIFICADO:
            print("ERRO: %s não é uma coluna do esquema do acervo unificado." % col)
            return

    # verifica se colunas existem no esquema unificado.
    for col in cols_fonte:
        if col not in df.columns:
            print("ERRO: %s não é uma coluna do esquema do acervo de entrada." % col)
            return

    if args.v:
        print("Esquema do acervo de entrada: ", cols_fonte)
        print("Projeção do esquema do acervo unificado: ", cols_destino)

    # 
    # Cada coluna no acervo de entrada corresponde a uma coluna no acervo unificado.
    # O trecho a seguir renomeias as colunas do acervo de entrada usando os nomes de
    # colunas correspondentes no acervo unificado. Essa transformação é útil pois
    # facilita a atualização do acervo unificado (que é realizada no desta função).
    #
    mapeamento_colunas = dict()
    for j in range (len(cols_fonte)):
        mapeamento_colunas[cols_fonte[j]] = cols_destino[j]  
    df.rename(columns=mapeamento_colunas, inplace=True)

    # Determina quais entradas são válidas e quais são inválidas no arquivo de entrada
    # (uma entrada é considerada válida se e somente se corresponde a um valor de ISBN válido)
    indices_entradas_invalidas = []
    indices_entradas_validas = []
    for index, row in df.iterrows():
        isbn = str(row['isbn13'])
        isbn = il.clean(isbn)
        isbn = il.to_isbn13(isbn)
        if isbn == 'nan' or isbn is None:
            indices_entradas_invalidas.append(index)
        else:
            indices_entradas_validas.append(index)

    # Filtra arquivo de entrada. Após essa operação, o arquivo possui apenas entradas válidas.
    df.drop(df.index[indices_entradas_invalidas],inplace=True)

    #
    # Dada uma entrada no arquivo a ser importado, ou essa entrada já existe no arquivo unificado, ou não.
    # O trecho a seguir identifica isso para cada entrada válida do arquivo a ser importado.
    #
    isbns_no_acervo_unif = df_unificado['isbn13'].tolist()

    # 'sanity check': o acervo unificado não pode conter entradas duplicadas.
    if len(set(isbns_no_acervo_unif)) != len(isbns_no_acervo_unif):
        print("ERRO GRAVE: acervo unificado contém duplicatas!")
        print(len(set(isbns_no_acervo_unif)) - len(isbns_no_acervo_unif))
        print([item for item, count in collections.Counter(isbns_no_acervo_unif).items() if count > 1])
        return

    isbns_no_arquivo_entrada = []
    temp = df['isbn13'].tolist()
    for t in temp:
        isbn = str(t)
        isbn = il.clean(isbn)
        isbn = il.to_isbn13(isbn)
        isbns_no_arquivo_entrada.append(isbn)

    df['isbn13'] = isbns_no_arquivo_entrada
    df.sort_values('isbn13',inplace=True)
    df.drop_duplicates(subset="isbn13", inplace=True)

    # 'sanity check': não queremos importar a mesma entrada mais de uma vez.
    isbns_no_arquivo_entrada = df['isbn13'].tolist()
    if len(set(isbns_no_arquivo_entrada)) != len(isbns_no_arquivo_entrada):
        print("ERRO GRAVE: acervo de entrada contém duplicatas!")
        print(len(indices_entradas_validas) - len(set(isbns_no_arquivo_entrada)))
        print([item for item, count in collections.Counter(isbns_no_arquivo_entrada).items() if count > 1])
        return

    entradas_ja_existentes = []
    entradas_novas = []

    isbns_no_acervo_entrada = df['isbn13'].tolist()

    for index, row in df.iterrows():
        isbn = str(row['isbn13'])
        isbn = il.clean(isbn)
        
        if il.is_isbn10(isbn):
            isbn13 = il.to_isbn13(isbn)
            if isbn13 in isbns_no_acervo_entrada:
                print("AVISO: duplicata no arquivo de entrada (cadastro com ISBN10 e ISBN13): %s" % isbn)
                return

        isbn = il.to_isbn13(isbn)

        if isbn == 'nan' or isbn is None:
            continue

        try:
            indice = isbns_no_acervo_unif.index(isbn)
        except ValueError:
            indice = -1;

        if indice >= 0:
            entradas_ja_existentes.append(index)
        else:
            entradas_novas.append(index)
            # print('***ERROR***')
            # print('row:', row)
            # print('row[isbn13]:', row['isbn13'])
            # print('isbn:', isbn)
            # return

    entradas_invalidas = 0
    entradas_atualizadas = 0
    entradas_inseridas = 0

    # cria dois novos dataframes, um para entradas novas e outro para entradas já existentes.
    df_inserir = df.loc[entradas_novas]
    df_atualizar = df.loc[entradas_ja_existentes]

    #
    # No acervo unificado, cada entrada é identificada pelo ISBN13. Portanto o trecho a seguir faz o mapeamento
    # dos valores de isbn provenientes do arquivo de entrada (que podem estar no formato ISBN10 ou ISBN13) para
    # ISBN13.
    #
    isbns_novos = df_inserir['isbn13'].tolist();
    isbns_existentes = df_atualizar['isbn13'].tolist();

    isbns_canonicos_novos = [il.to_isbn13(i) for i in isbns_novos]
    df_inserir['isbn13'] = isbns_canonicos_novos

    isbns_canonicos_existentes = [il.to_isbn13(i) for i in isbns_existentes]
    df_atualizar['isbn13'] = isbns_canonicos_existentes

    #
    # realiza as alterações pertinentes sobre o acervo unificado: 
    #    - entradas novas são inseridas (concat)
    #    - entradas já existentes são atualizadas (merge e update)
    #
    df_inserir.reset_index(drop=True, inplace=True)
    df_atualizar.reset_index(drop=True, inplace=True)
    if args.v:
        print("Entradas atuais: ", len(df_unificado.index))
        print("Novas entradas: ", len(df_inserir.index))
        print("Entradas a atualizar: ", len(df_atualizar.index))

    tamanho_acervo = len(df_unificado.index)

    print("Antes da importação, acervo unificado contém %d entrada(s)." % tamanho_acervo)

    df_unificado = pd.concat([df_unificado, df_inserir], axis=0, sort=False)
    df_unificado.reset_index(drop=True, inplace=True)

    result = df_unificado[['isbn13']].merge(df_atualizar, how="left")
    df_unificado.update(result)
    df_unificado.reset_index(drop=True, inplace=True)

    tamanho_acervo = len(df_unificado.index)

    print("Após a importação, acervo unificado contém %d entrada(s)." % tamanho_acervo)

    # df_unificado.set_index('isbn13',inplace=True)
    df_unificado.to_json(JSON_ACERVO_UNIFICADO)


def generate_xml():

    xml = json2xml.Json2xml(acervo_dict).to_xml()
    
    if(xml):
        path = './xmlfiles'
        
        if not os.path.isdir(path):
           os.mkdir(path)
        
        myfile = open(JSON_ACERVO_UNIFICADO, "w")
        myfile.write(xml)
    
        print("Xml e json salvos nas pastas xmlfiles e jsonfiles, respectivamente, com o nome de dadosuniversidades.")
        
        
def main():

    parser = argparse.ArgumentParser(description="Importador de acervos de bibliotecas.")
    parser.add_argument("-i", help = "nome do arquivo de entrada (contendo acervo a ser importado), no formato csv ou xlsx", required=True)
    parser.add_argument("-v", help = "modo 'verboso' de execução", action = "store_true")
    parser.add_argument("-isbn", help = "especifica nome da coluna relativa ao ISBN no arquivo de entrada", required=True)
    parser.add_argument("-fonte", help = "lista com nomes de colunas a importar", required=True)
    parser.add_argument("-destino", help = "lista com nomes de colunas correspondentes na base unificada", required=True)
    parser.add_argument("-json", help = "gera o arquivo json", action = "store_true")

    args = parser.parse_args()

    input_file = 'data/' + args.i

    if args.v:
        # imprime o esquema (nomes das colunas) do arquivo de acervo
        imprimir_esquema(input_file)
    
        # imprime as primeiras linhas do arquivo a ser importado, para inspeção
        imprimir_primeiras_linhas(input_file)

    importar_acervo_bibliotecario(args, input_file, args.isbn, args.fonte, args.destino)
    
if __name__ == "__main__":
    main()


