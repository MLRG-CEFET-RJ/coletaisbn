# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:05:33 2019

@author: Eduardo Bezerra & Daniel Favoreto
"""

import argparse
import json
import os
import re
import isbnlib
from crossref.restful import Works
from isbnlib.registry import bibformatters

def consulta_isbn(isbn, library):
    lista_isbns = []
    lista_isbns.append(isbn)
    consulta(lista_isbns, library)

def consulta_isbns(isbns_file, library):
    file = open('{}'.format(isbns_file),'r', encoding='utf8')
    lista_isbns = [linha.rstrip('\n') for linha in file]
    consulta(lista_isbns, library)

def consulta(lista_isbns, servico):
    formatador_json = bibformatters['json']
    isbn_dict = {}

    if servico == 'gbooks':
        for isbn in lista_isbns:
            try:
                data = isbnlib.meta(isbn, service='goob')
                isbn_dict[str(isbn)] = formatador_json(data)
            except isbnlib.dev.DataNotFoundAtServiceError:
                print("Entrada com ISBN %s não foi encontrada no serviço %s." % (isbn, servico))    
    elif servico == 'openl':
        for isbn in lista_isbns:
            try:
                a = isbn
                a = a.strip()
                data = isbnlib.meta(isbn, service = 'openl')
                isbn_dict[str(isbn)] = formatador_json(data)
            except isbnlib.dev.DataNotFoundAtServiceError:                    
                print("Entrada com ISBN %s não foi encontrada no serviço %s." % (isbn, servico))
    elif servico == 'crref':
        for isbn in lista_isbns:
            a = isbn
            a = a.strip()
            works = Works()
            a = works.filter(isbn = str(a))
            b = []
            for item in a:
                b.append((item))
            isbn_dict[str(a)] = b
    else:
        print("ERRO: Serviço de consulta desconhecido.")

    if isbn_dict:
        with open('./' + servico + '.json', 'w') as outfile:
            json.dump(isbn_dict, outfile)
    
 
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", help = "Serviço a ser usado para buscas. Opções:"
                                    "gbooks (Google Books), openl (Open Library), crref (Cross Ref)", required=True)
    parser.add_argument("-isbn", help = "Número isbn para usar na busca."
                                    "Saída: Um arquivo json com a (única) entrada recuperada.")
    parser.add_argument("-isbns", help = "Arquivo txt ou csv contendo um número isbn em cada linha para usar na busca."
                                    "Saída: Um arquivo json com as entradas recuperadas.")

    args = parser.parse_args()

    if args.isbn is None and args.isbns is None:
        print("Nenhum isbn fornecido para busca.")
    elif args.isbn is not None and args.isbns is not None:
        print("Forneça ou apenas um número isbn, ou um arquivo com números isbn.")
    elif args.isbns is None:
        consulta_isbn(args.isbn, args.s)
    elif args.isbn is None:
        consulta_isbns(args.isbns, args.s)

if __name__ == "__main__":
    main()

