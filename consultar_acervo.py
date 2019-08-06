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

JSON_ACERVO_UNIFICADO = 'data/acervo_unificado.json'

def main():

    parser = argparse.ArgumentParser(description="Permite consultar acervo unificado.")
    parser.add_argument("-isbn", help = "especifica o valor do ISBN13 a ser consultado", required=True)

    args = parser.parse_args()

    if not il.is_isbn13(args.isbn):
        print("ERRO: argumento não é um ISBN válido: %s" % args.isbn)
        return 

    if not os.path.isfile(JSON_ACERVO_UNIFICADO):
        print("ERRO: acervo unificado não encontrado")
        return 

    df_unificado = pd.read_json(JSON_ACERVO_UNIFICADO, dtype=str)

    for index, row in df_unificado.iterrows():
        isbn = str(row['isbn13'])
        if isbn == args.isbn:
            print(index)
            print(il.to_isbn10(isbn))
            print(row)

if __name__ == "__main__":
    main()


