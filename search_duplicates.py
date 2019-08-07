# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 14:17:50 2019

@author: Daniel
"""

import pandas as pd
import disamby.preprocessors as pre
from disamby import Disamby
import argparse
import re

class Duplicates():
    def __init__(self, nome_arquivo, nome_coluna):
        self.nome_arquivo = nome_arquivo
        self.nome_coluna  = nome_coluna
        
    def find_duplicates(self):
        
        self.load_dataset()
        
        pipeline = [
            pre.normalize_whitespace,
            pre.remove_punctuation,
            lambda x: pre.trigram(x) + pre.split_words(x)
        ]
        
        dis = Disamby(self.df_coluna, pipeline)
        
        self.lista_de_sets = dis.disambiguated_sets(threshold=0.5)
        self.criar_lista_de_posicoes()
        self.generate_csv()
        
    def criar_lista_de_posicoes(self):
        self.lista_de_posicoes = []
        for sets in self.lista_de_sets:
            posicoes = list(sets)
            if len(posicoes) == 2:
                self.lista_de_posicoes.append((posicoes))
    
    def generate_csv(self):
        positions_df = pd.DataFrame(self.lista_de_posicoes)
        positions_df.to_csv('duplicates_list.csv', index = False)
    
    def load_dataset(self):
        path = 'new_csvs/'
        extensao_arquivo = re.search('\.(.*)', self.nome_arquivo).group()
        if(extensao_arquivo == ".csv"):
            self.df = pd.read_csv(path+self.nome_arquivo)
            self.df_coluna = self.df[self.nome_coluna].astype(str)
        else:
            self.df = pd.read_excel(path+self.nome_arquivo)
            self.df_coluna = self.df[self.nome_coluna].astype(str)
        
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",  help="Nome do arquivo de entrada", required=True)
    parser.add_argument("-col",help="Nome da coluna para busca por duplicatas", required=True)
    
    args   = parser.parse_args()
    
    duplicates = Duplicates(args.f,args.col)
    duplicates.find_duplicates()
    
if __name__ == "__main__":
    main()

        



