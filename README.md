# BibliCAPES

Nesse desafio iremos tentar buscar dados isbn como autores,titulo,obra,etc... e formatar tudo em um arquivo json ou xml.

## Pré-requisitos:

>pip install disamby<br />
>pip install pandas<br />
>pip install argparse<br />
>pip install crossrefapi<br />
>pip install json2xml<br />


## Modo de uso:

A busca pelos dados consiste em duas classes. <br />
A primeira busca pode ser feita com dados de universidades como CEFET,UFF,etc. Para utilizar essa busca, é necessario que os dados estejam no formato csv ou xlsx. Note que os dados no formato csv possibilitam uma busca visivelmente mais rapida que dados no formato xlsx. O resultado dessa classe irá gerar uma lista com numeros isbn para que a segunda busca também possa ser possível.<br />
A segunda busca pode ser feita na nuvem, com bibliotecas como googlebooks, openlibrary ou crossref. Note que para utilizar essa busca é necessario uma lista com numeros isbn.

### Exemplos:

#### Etapa 1:
Para fazer uma busca com os dados de universidades, primeiro coloque os arquivos na pasta Acervos:
>Entrada:<br />
>cd acervos<br />
>dir<br />
>Saida:<br />
![Capturar2](https://user-images.githubusercontent.com/39687418/62415608-fea61d80-b602-11e9-80dd-2dca47c4fe55.PNG)

Aqui podemos ver que temos dois arquivos, acervo-cefetrj.csv e acervo-uff.xlsx<br/>

#### Etapa 2:

Podemos prosseguir então, para ver o conteudo desses acervos. Para ver quais são as colunas dos arquivos, basta escrever:
>Entrada:<br />
>python ler_acervo.py -f acervo-cefetrj.csv -t<br />
>Saida:<br />
![Capturar4](https://user-images.githubusercontent.com/39687418/62415611-02d23b00-b603-11e9-8747-fe25565966b4.PNG)<br />
>Entrada:<br />
>python ler_acervo.py -f acervo-uff.xlsx -t<br />
>Saida:<br />
![Capturar13](https://user-images.githubusercontent.com/39687418/62415624-17aece80-b603-11e9-9bff-f8ec3a8b2309.PNG)

Aqui podemos ver que o arquivo do cefet contem os seguintes campos: TITULO, ASSUNTOS, AUTORES, OBRA, IDIOMA, ANO, DATA_ATUALIZACAO, MATERIAL, CLASSIFICACAO, TIPO_MATERIAL, ISBN_ISSN, AUTOR_PRINCIPAL, EDITORA, EDICAO. Enquanto o arquivo da uff contem 31 campos.

#### Etapa 3:
Pronto. Agora que sabemos quais são as colunas dos arquivos, podemos inspecionar o que tem dentro dessas colunas para determinar se queremos ou não por essas colunas no nosso futuro arquivo json ou xml. Para inspecionar o que tem dentro das colunas, você pode escrever:
>Entrada:<br />
>python ler_acervo.py -f acervo-cefetrj.csv -col ISBN_ISSN -c<br />
>Saida:<br />
![Capturar6](https://user-images.githubusercontent.com/39687418/62415615-0796ef00-b603-11e9-9307-920edcf6a03b.PNG)

Note que essa etapa é importante, pois só podemos continuar com as próximas etapas após termos determinado qual dessas colunas contem os numeros isbn. Isso pode ser um pouco difícil, pois nem sempre é claro quais dessas colunas contém os numeros ISBN. No dataset da UFF por exemplo, os números ISBN ficam dentro da coluna ESCALA.
>Entrada:<br />
>python ler_acervo.py -f acervo-uff.xlsx -col ESCALA -c<br />
>Saida:<br />
![Capturar16](https://user-images.githubusercontent.com/39687418/62415731-0070e080-b605-11e9-8aee-b63162b1fc35.PNG)

#### Etapa 4:
Agora que já sabemos qual coluna contém os números ISBN, precisamos gerar a lista com os números ISBN. Isso é essencial e precisa ser feito para que o restante do código possa funcionar. Essa etapa é necessária porque a chave que iremos usar para criar o arquivo JSON são os números ISBN. Como nem todas as linhas das planilhas do CEFET e da UFF contém um número ISBN, esse comando irá reduzir o arquivo csv ou xlsx para um novo arquivo, que terá todas as linhas sem números ISBN removidas do arquivo principal.
>Entradas:<br />
>python ler_acervo.py -f acervo-cefetrj.csv -col ISBN_ISSN -list<br />
>python ler_acervo.py -f acervo-uff.xlsx -col ESCALA -list<br />

A lista com os números isbn ficará guarda na pasta ISBN_lists, enquanto o novo arquivo csv simplificado ficará guardado na pasta New_csvs

#### Etapa 5:
A próxima etapa consiste em gerar os arquivos xml ou json. O comando que faz isso possibilita que você escolha quais colunas da planilha deseja adicionar ao arquivo json ou xml. Note que o comando -json irá gerar apenas um arquivo json, enquanto que o comando -xml irá gerar ambos.
>Entradas:<br />
>python ler_acervo.py -f acervo-cefetrj.csv -col TITULO -to titulo -json<br />
>python ler_acervo.py -f acervo-cefetrj.csv -col TITULO,ASSUNTOS -to titulo,assuntos -json<br />
>python ler_acervo.py -f acervo-cefetrj.csv -col TITULO,ASSUNTOS,AUTORES,OBRA,IDIOMA -to titulo,assuntos,autores,obra,idioma -xml<br />
>python ler_acervo.py -f acervo-cefetrj.csv -col TITULO,ASSUNTOS,AUTORES,OBRA,IDIOMA,ISBN_ISSN -to titulo,assuntos,autores,obra,idioma,isbn -xml<br />

O arquivo json gerado ficará guardado na pasta Jsonfiles com o nome dadosuniversidades.json, equanto o arquivo xml ficará guardado na pasta
xmlfiles com o nome dadosuniversidades.xml

#### Comandos úteis:<br />
##### Para inspecionar o nome das colunas:<br />
>python ler_acervo.py -f file_name -t<br />
##### Para inspecionar o conteúdo das colunas:<br />
>python ler_acervo.py -f file_name -col col_name -c<br />
##### Para gerar a lista com números ISBN:<br />
>python ler_acervo.py -f file_name -col isbn_col -list<br />
##### Para gerar o arquivo json com as colunas do arquivo csv ou xlsx:<br />
>python ler_acervo.py -f file_name -col col1,col2,col3,...,coln -to col1,col2,col3,...,coln -json<br />
##### Para gerar o arquivo json e xml com as colunas do arquivo csv ou xlsx:<br />
>python ler_acervo.py -f file_name -col col1,col2,col3,...,coln -to col1,col2,col3,...,coln -xml

### Exemplos na nuvem:

Para buscar dados de plataformas como googlebooks, crossref e openlibrary, é necessário ter uma lista com números ISBN.
#### Googlebooks:
>python requisicao_dados.py -f isbns.txt -l gbooks
#### Openlibrary:
>python requisicao_dados.py -f isbns.txt -l openl
#### Crossref:
>python requisicao_dados.py -f isbns.txt -l crossref

### Busca por duplicatas:

O código procura por campos que contenham o mesmo autor. Quando existem erros de digitação no nome, o programa irá definir um grau de similaridade entre eles. Caso seja decidido que existem duplicatas, o código irá retornar uma lista com a posição das mesmas.Exemplo:

>python search_duplicates.py -f acervo-cefetrj.csv -col AUTORES










