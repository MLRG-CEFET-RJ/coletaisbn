# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:05:33 2019

@author: Daniel
"""

import argparse
import googlebooks
import json
import os
import re
import openlibrary
from crossref.restful import Works

#Classe para gerar os arquivos json de uma lista com numeros isbn
class Isbn_list:
    
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
                isbn_dict[str(isbn)] = data
            if not os.path.isdir(path):
                os.mkdir(path)          
            name = re.search(r'.*(?=\.)',self.file_name).group()
            with open('{}/gbooks_{}.json'.format(path,name), 'w') as outfile:
                json.dump(isbn_dict, outfile)
        
        elif(self.library=='openl'):
            
            final_dict = {}
            file = open('{}'.format(self.file_name),'r',encoding='utf8')
            for isbn in file:
                try:
                    a = isbn
                    a = a.strip()
                    api = openlibrary.Api()
                    book = api.get_book("{}".format(a))
                    
                    my_dict = {}
                    authors = book.authors    
                    publishers = book.publishers
                    identifiers = book.identifiers
                    classifications = book.classifications
                    links = book.links
                    weight = book.weight
                    title = book.title
                    subtitle = book.subtitle
                    url = book.url
                    number_of_pages = book.number_of_pages
                    cover = book.cover
                    subjects = book.subjects
                    publish_date = book.publish_date
                    excerpts = book.excerpts
                    publish_places = book.publish_places
                    
                    author_list = []
                    for author in authors:
                        a = author.get_name()
                        author_list.append((a))
                    
                    publisher_list=[]
                    for publisher in publishers:
                        a = publisher.get_name()
                        publisher_list.append((a))
                    
                    my_dict['authors'] = author_list
                    my_dict['publishers'] = publisher_list
                    my_dict['identifiers'] = identifiers
                    my_dict['classifications'] = classifications
                    my_dict['links'] = links
                    my_dict['weight'] = weight
                    my_dict['title'] = title
                    my_dict['subtitle'] = subtitle
                    my_dict['url'] = url
                    my_dict['number_of_pages'] = number_of_pages
                    my_dict['cover'] = cover
                    my_dict['subjects'] = subjects
                    my_dict['publish_date'] = publish_date
                    my_dict['excerpts'] = excerpts
                    my_dict['publish_places'] = publish_places
                    
                    final_dict[str(isbn)] = my_dict
                except KeyError:
                    print("erro na chave {}".format(isbn))
                    
            if not os.path.isdir(path):
                os.mkdir(path)
            name = re.search(r'.*(?=\.)',self.file_name).group()
            with open('{}/openl_{}.json'.format(path,name), 'w') as outfile:
                json.dump(final_dict, outfile)
        
        elif(self.library=='crossref'):
            

            my_dict = {}
            file = open('{}'.format(self.file_name),'r',encoding='utf8')
            
            for isbn in file:
                a = isbn
                a = a.strip()
                works = Works()
                a = works.filter(isbn=str(a))
                b = []
                for item in a:
                    b.append((item))
                my_dict[str(a)]=b
                
            if not os.path.isdir(path):
                os.mkdir(path)
            name = re.search(r'.*(?=\.)',self.file_name).group()     
            with open('{}/crosf_{}.json'.format(path,name), 'w') as outfile:
                json.dump(my_dict, outfile)
        
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
            with open('{}/gbooks_{}.json'.format(path,self.isbn), 'w') as outfile:
                json.dump(data, outfile)
    
        elif(self.library=='openl'):
            
            try:
                api = openlibrary.Api()    
                book = api.get_book("{}".format(self.isbn))
                my_dict = {}
                
                authors = book.authors    
                publishers = book.publishers
                identifiers = book.identifiers
                classifications = book.classifications
                links = book.links
                weight = book.weight
                title = book.title
                subtitle = book.subtitle
                url = book.url
                number_of_pages = book.number_of_pages
                cover = book.cover
                subjects = book.subjects
                publish_date = book.publish_date
                excerpts = book.excerpts
                publish_places = book.publish_places
                
                author_list = []
                for author in authors:
                    a = author.get_name()
                    author_list.append((a))
                
                publisher_list=[]
                for publisher in publishers:
                    a = publisher.get_name()
                    publisher_list.append((a))
                
                my_dict['authors'] = author_list
                my_dict['publishers'] = publisher_list
                my_dict['identifiers'] = identifiers
                my_dict['classifications'] = classifications
                my_dict['links'] = links
                my_dict['weight'] = weight
                my_dict['title'] = title
                my_dict['subtitle'] = subtitle
                my_dict['url'] = url
                my_dict['number_of_pages'] = number_of_pages
                my_dict['cover'] = cover
                my_dict['subjects'] = subjects
                my_dict['publish_date'] = publish_date
                my_dict['excerpts'] = excerpts
                my_dict['publish_places'] = publish_places
                
                if not os.path.isdir(path):
                    os.mkdir(path)
                
                with open('{}/openl_{}.json'.format(path,self.isbn), 'w') as outfile:
                    json.dump(my_dict, outfile)
            except (KeyError):
                print("erro na chave {}".format(self.isbn))
                
    
        elif(self.library=='crosf'):
            my_dict={}
            works = Works()
            a = works.filter(isbn=str(self.isbn))
            b = []
            for item in a:
                b.append((item))
            my_dict[self.isbn]=b
            with open('{}/crosf_{}.json'.format(path,self.isbn), 'w') as outfile:
                json.dump(my_dict, outfile)
    
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
    json_output = Isbn_list(args.f,args.l)
    json_output.generate_json()


