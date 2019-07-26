# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:05:33 2019

@author: Daniel
"""

import argparse
import googlebooks
import openlibrary
from crossref.restful import Works
import json
import os
import re

#Classe para gerar os arquivos json de uma lista com numeros isbn
class Isbn_file:
    
    def __init__(self, file_name, library):
        self.file_name = file_name
        self.library = library
        
    def generate_json(self):
        if(self.library=='gbooks'):
            isbn_dict={}
            file = open('{}'.format(self.file_name),'r',encoding='utf8')
            #Le linha por linha do arquivo e cria um dicionário
            for isbn in file:
                api = googlebooks.Api()
                data = api.list('isbn:{}'.format(isbn))
                isbn_dict[isbn] = data
            if not os.path.isdir(path):
                os.mkdir(path)          
            name = re.search(r'.*(?=\.)',self.file_name).group()
            with open('{}/Json_{}.json'.format(path,name), 'w') as outfile:
                json.dump(isbn_dict, outfile)
        
        elif(self.library=='openl'):
            print("Voce quer os dados da open library")
        
        elif(self.library=='crosf'):
            print("Voce quer os dados do crossref")
        
        else:
            print("Biblioteca inserida nao reconhecida")
        

class Isbn:
    def __init__(self, isbn, library):
        self.isbn = isbn
        self.library = library
    
    def generate_json(self):
        if(self.library=='gbooks'):
            api = googlebooks.Api()
            data = api.list('isbn:{}'.format(self.isbn))
            if not os.path.isdir(path):
                os.mkdir(path)
            with open('{}/Json_{}.json'.format(path,self.isbn), 'w') as outfile:
                json.dump(data, outfile)
    
        elif(self.library=='openl'):
            print("Voce quer os dados da open library")
    
        elif(self.library=='crosf'):
            print("Voce quer os dados do crossref")
    
        else:
            print("Biblioteca inserida nao reconhecida")


parser = argparse.ArgumentParser()
parser.add_argument("-i",help = "Numero isbn usado para buscas."
                                "Saida: Um arquivo json")
parser.add_argument("-l",help = "Biblioteca usada para buscas.Opcoes:"
                                "gbooks, openl, crossref",required=True)
parser.add_argument("-f",help = "Arquivo txt ou csv contendo um numero isbn em cada linha para buscas."
                                "Saida: Um arquivo json")
parser.add_argument("-o",help = "Nome do arquivo de Saída."
                                "Default:Jsonfiles/Json_n")

args = parser.parse_args()

path = './Jsonfiles'

if args.i is None and args.f is None:
    print("Nenhum numero isbn inserido")
    
elif(args.i is not None and args.f is not None):
    print("Insira apenas um numero isbn ou uma lista com numeros isbn")

elif(args.f is None):
    json_output = Isbn(args.i,args.l)
    json_output.generate_json()
            
elif(args.i is None):
    json_output = Isbn_file(args.f,args.l)
    json_output.generate_json()
    

    
    
