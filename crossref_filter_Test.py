# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 02:47:32 2019

@author: Daniel
"""

from isbnlib import meta
from isbnlib.registry import bibformatters
from isbnlib import doi
from isbnlib import doi2tex
from isbnlib import cover
from isbnlib import info
from crossref.restful import Works

works = Works()
SERVICE = 'goob'

# now you can use the service
isbn = '9780446310789'
bibtex = bibformatters['bibtex']
doin = doi(isbn)
print(bibtex(meta(isbn, SERVICE)))
print(doi(isbn))
print(doi2tex(doin))
doi2tex(doin)

cover(isbn)

info(isbn)

a = works.doi(doin)
print(doin)

works = Works()

works.select('ISBN')
c = works.filter(isbn='9783319081403').select('author')
for CU in works.filter(isbn='9783319081403').select('author'):
    c = CU
print(type(c))
    
c = works.filter(isbn='9780446310789').select('author')
for CU in works.filter(isbn='9780446310789').select('author'):
    c = CU
print(type(c))
    


for i in works.filter(isbn='9780446310789'):
    a.append((i))
for i in works.query(title='To Kill A Mockingbird', author='Harper Lee', publisher_name='Grand Central Publishing').select('ISBN'):
    print(i)