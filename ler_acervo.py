# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 18:27:10 2019

@author: Daniel
"""

import pandas as pd
import numpy as np
import re
import argparse
import os
import json
from json2xml import json2xml

def print_coluna(validator,file_name,titulo):
    if(validator =='.csv'):
        df = pd.read_csv(file_name,usecols =   [titulo])
        print(df[titulo])
    else:
        df = pd.read_excel(file_name,usecols = [titulo])
        print(df[titulo])
        
def print_titulos(validator,file_name):
    if(validator =='.csv'):
        print(pd.read_csv(file_name,nrows=1).columns)
    else:
        print(pd.read_excel(file_name,nrows=1).columns)
        
class Acervo():   
    def __init__(self, df, isbn_header, file):
        self.df = df
        self.isbn_header = isbn_header
        self.file = file
        
    def only_isbn(self):
        
        path_df   = './New_csvs'
        path_list ='./ISBN_lists'
        
        if not os.path.isdir(path_df):
            os.mkdir(path_df)
        if not os.path.isdir(path_list):
            os.mkdir(path_list)
            
        if(self.isbn_header==None):
            print("Erro:indique o titulo que contem os numeros isbn")
        else:
            k = self.df[self.isbn_header].values
            k = np.array(k).reshape(k.shape[0],1).astype(dtype='str')
            
            positions_list = []
            list_ = []
            for (positions,name) in enumerate (k):
                pattern = re.search("[0-9]{10,13}",str(name))
                if pattern is None:
                    positions_list.append(positions)
                else:
                    list_.append((pattern.group()))
            
            self.df = self.df.drop(self.df.index[positions_list])
            self.df[self.isbn_header]=list_
            self.df.to_csv('{}/{}_novo.csv'.format(path_df,self.file),index=None)
            list_ = pd.DataFrame(list_)
            list_.to_csv('{}/{}_isbn.csv'.format(path_list,self.file),index=None)
        
        print("Lista com numeros isbn gerada.")
            
class Constructor():   
    def __init__(self,df,isbn_list,isbn_title,new_title,xml):
        self.df          = df
        self.isbn_list   = isbn_list
        self.isbn_title  = isbn_title
        self.new_title   = new_title 
        self.xml         = xml
        
    def generate_json(self):
        
        path = './Jsonfiles'
        
        if os.path.isfile('{}/dadosuniversidades.json'.format(path)):
            with open(path+'/dadosuniversidades.json') as json_file:
                my_dict = json.load(json_file)
        else:
            my_dict = {}
            
        isbn_list = list(self.isbn_list['0'])
        
        a = self.new_title.split(',')
        b = self.isbn_title.split(',')
        
        for j in range (len(a)):
            
            titulo_list = list(self.df[b[j]])
            concatenate_list = []
            
            for isbn in isbn_list:
                if (not ('{}'.format(isbn) in my_dict)):
                    my_dict[str(isbn)] = {}
                
            for i, titulos in enumerate(titulo_list):
                concatenate_list.append(((isbn_list[i]),(a[j],titulos)))
                
            for data in concatenate_list:
                my_dict[str(data[0])][data[1][0]]=data[1][1]
                
        if not os.path.isdir(path):
            os.mkdir(path)
            
        with open('{}/dadosuniversidades.json'.format(path), 'w') as outfile:
                json.dump(my_dict, outfile)
                print("Arquivo json gerado com sucesso.")
        
        xml=json2xml.Json2xml(my_dict).to_xml()
        
        if(self.xml):
            path = './xmlfiles'
            
            if not os.path.isdir(path):
               os.mkdir(path)
            
            myfile = open("{}/dadosuniversidades.xml".format(path), "w")
            myfile.write(xml)
        
            print("Xml e json salvos nas pastas xmlfiles e jsonfiles, respectivamente, com o nome de dadosuniversidades.")
        
        
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",help = "acervo no formato csv ou xlsx",required=True)
    parser.add_argument("-t",help = "usado para obter os titulos do arquivo",action = "store_true")
    parser.add_argument("-col",help = "nome do titulo")
    parser.add_argument("-c",help = "usado para inspecionar o conteudo do titulo",action = "store_true")
    parser.add_argument("-list",help = "usado para gerar dois novos arquivos csv",action = "store_true")
    parser.add_argument("-json",help = "usado para gerar o arquivo json",action = "store_true")
    parser.add_argument("-to",help= "titulo novo")
    parser.add_argument("-xml",help="usado para gerar o arquivo xml",action = "store_true")

    args      = parser.parse_args()
    validator = re.search('\.(.*)',args.f).group()
    name      = re.search('.*(?=\.)',args.f).group()
    
    if (args.t):
        print_titulos(validator, 'acervos/'+args.f)
    
    if(args.c):
        if(args.col==None):
            print("Erro: Voce esqueceu o nome do titulo")
        else:
            print_coluna(validator,'acervos/'+args.f,args.col)
           
    if(args.list):
        if validator == '.csv':
            df = Acervo(pd.read_csv('acervos/'+args.f),args.col, name)
            df.only_isbn()
        else:
            df = Acervo(pd.read_excel('acervos/'+args.f),args.col, name)
            df.only_isbn()
        
    if(args.json)or(args.xml):
        if validator == '.csv':
            name_df   = re.search('.*(?=\.)',args.f).group() + "_novo.csv" 
            name_list = re.search('.*(?=\.)',args.f).group() + "_isbn.csv"
            df        = pd.read_csv('New_csvs/'+name_df)
            isbn_list = pd.read_csv('ISBN_lists/'+name_list)
            constructor = Constructor(df, isbn_list, args.col, args.to,args.xml)
            constructor.generate_json()
        else:
            name_df   = re.search('.*(?=\.)',args.f).group() + "_novo.csv" 
            name_list = re.search('.*(?=\.)',args.f).group() + "_isbn.csv"
            df        = pd.read_csv('New_csvs/'+name_df)
            isbn_list = pd.read_csv('ISBN_lists/'+name_list)
            constructor = Constructor(df, isbn_list, args.col, args.to,args.xml)
            constructor.generate_json()
    
if __name__ == "__main__":
    main()

path = './Jsonfiles'

if os.path.isfile('{}/dadosuniversidades.json'.format(path)):
    with open(path+'/dadosuniversidades.json') as json_file:
        my_dict = json.load(json_file)

