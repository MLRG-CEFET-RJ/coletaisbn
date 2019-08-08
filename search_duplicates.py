# -*- coding: utf-8 -*-
"""
Created on Jul  4 14:17:50 2019

@author: Daniel Favoreto & Eduardo Bezerra
"""

import pandas as pd
import disamby.preprocessors as pre
from disamby import Disamby
import argparse
import re
import sys

JSON_ACERVO_UNIFICADO = "./data/acervo_unificado.json"

class Desambiguador():
    def __init__(self, nome_arquivo, nome_coluna):
        self.nome_arquivo = nome_arquivo
        self.nome_coluna  = nome_coluna
        
    def analisar(self):
        
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
        if self.nome_arquivo is None:
            self.nome_arquivo = JSON_ACERVO_UNIFICADO
            self.df = pd.read_json(self.nome_arquivo, dtype=str)
        else:
            extensao_arquivo = re.search('\.(.*)', self.nome_arquivo).group()
            if(extensao_arquivo == ".csv"):
                self.df = pd.read_csv(self.nome_arquivo)
            else:
                self.df = pd.read_excel(self.nome_arquivo)

        if self.nome_coluna in self.df.columns:
            self.df_coluna = self.df[self.nome_coluna].astype(str)
        else: 
            print("ERRO: coluna não encontrada: %s.\n" % self.nome_coluna)
            sys.exit(1)
        
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",  help="Nome do arquivo (acervo) de entrada. "
        "Opcional. Se não for especificado, considera que a análise deve ser realizada no acervo unificado.")
    parser.add_argument("-col",help="Nome da coluna sobre a qual realizar a análise.", required=True)
    
    args   = parser.parse_args()

    duplicates = Desambiguador(args.i,args.col)
    duplicates.analisar()
    
if __name__ == "__main__":
    main()

        



