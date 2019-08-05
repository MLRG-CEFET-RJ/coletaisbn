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

JSON_ACERVO_UNIFICADO = './data/acervo_unificado.json'
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

    tamanho_acervo = len(df_unificado.index)

    extensao_arquivo = re.search('\.(.*)', input_file).group()
    if extensao_arquivo =='.csv':
        df = pd.read_csv(input_file, dtype=str)
    elif extensao_arquivo =='.xlsx':
        df = pd.read_excel(input_file, dtype=str)

    df = df[cols_fonte]

    mapeamento_colunas = dict()
    for j in range (len(cols_fonte)):
        mapeamento_colunas[cols_fonte[j]] = cols_destino[j]  

    df.rename(columns=mapeamento_colunas, inplace=True)

    print("Antes da importação, acervo unificado contém %d entrada(s)." % tamanho_acervo)

    #TODO: verificar se essas colunas existem nos dfs de entrada e unificado.
    if args.v:
        print(cols_fonte)
        print(cols_destino)

    if len(cols_fonte) != len(cols_destino):
        print("ERRO: listas de colunas fonte e destino devem ter mesmo tamanho.")
        return False

    indices_entradas_invalidas = []
    for index, row in df.iterrows():
        isbn = str(row['isbn13'])
        isbn = il.clean(isbn)
        isbn = il.to_isbn13(isbn)
        if isbn == 'nan' or isbn is None:
            indices_entradas_invalidas.append(index)

    df.drop(df.index[indices_entradas_invalidas],inplace=True)

    isbns_no_acervo_unif = df_unificado['isbn13'].tolist()

    entradas_ja_existentes = []
    entradas_novas = []

    for index, row in df.iterrows():
        isbn = str(row['isbn13'])
        isbn = il.clean(isbn)
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

    entradas_invalidas = 0
    entradas_atualizadas = 0
    entradas_inseridas = 0

    df_inserir = df.loc[entradas_novas]
    df_atualizar = df.loc[entradas_ja_existentes]

    isbns_novos = df_inserir['isbn13'].tolist();
    isbns_existentes = df_atualizar['isbn13'].tolist();

    isbns_canonicos_novos = [il.to_isbn13(i) for i in isbns_novos]
    df_inserir['isbn13'] = isbns_canonicos_novos

    isbns_canonicos_existentes = [il.to_isbn13(i) for i in isbns_existentes]
    df_atualizar['isbn13'] = isbns_canonicos_existentes

    df_unificado = df.append(df_inserir, ignore_index=True)

    print("inserido:")
    print(df_unificado.columns)
    print(df_unificado)

    result = df_unificado[['isbn13']].merge(df_atualizar, how="left")

    print("atualizado:")
    print(df_unificado.columns)
    print(df_unificado)

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

    input_file = './data/' + args.i

    if args.v:
        # imprime o esquema (nomes das colunas) do arquivo de acervo
        imprimir_esquema(input_file)
    
        # imprime as primeiras linhas do arquivo a ser importado, para inspeção
        imprimir_primeiras_linhas(input_file)

    importar_acervo_bibliotecario(args, input_file, args.isbn, args.fonte, args.destino)
    
if __name__ == "__main__":
    main()


