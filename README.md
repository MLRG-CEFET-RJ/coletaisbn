# ColetaISBN

O ColetaISBN é um conjunto de scripts em Python que permite importar dados bibliográficos a partir de alguns Web services disponíveis publicamente, assim como permite importar acervos bibliográficos provenientes de bibliotecas públicas ou particulares. Em conjunto, essas duas funcionalidades permitem construir uma base unificada de informações (metadados) sobre livros. O ColetaISBN também fornece uma funcionalidade para desambiguação de nomes de entidades. Um breve vídeo (2min) com uma demonstração de uso das funcionalidades fornecidas pelo ColetaISBN pode ser acessado [aqui](https://www.dropbox.com/s/asmkw49h3j3rmc9/ColetaISBN.mov?dl=0). 

## Dependências

>pip install disamby<br />
>pip install pandas<br />
>pip install argparse<br />
>pip install crossrefapi<br />
>pip install json2xml<br />
>pip install isbnlib<br />

## Funcionalidades

### Importação de Acervos Bibliotecários

Essa funcionalidade permite que o acervo bibliográfico de uma biblioteca seja adicionado (i.e., importado) ao repositório unificado do ColetaISBN. Nossa ideia nessa funcionalidade foi permitir que o ColetaISBN pudesse aproveitar os acervos bibliográficos já existentes em diferentes instituições de ensino e pesquisa de nosso país para alimentar gradativamente o a base unificada de livros do sistema. Dessa forma, se alguma biblioteca (pública ou particular) disponibiliza total ou parcialmente seu acervo de livros, é possível por meio desta funcionalidade, importar este acervo para a base unificada do ColetaISBN.

Para realizar os testes desta funcionalidade, durante a execução deste projeto, conseguimos dois acervos, provenientes do das bibliotecas do CEFET/RJ (http://www.cefet-rj.br/index.php/bibliotecas) e da UFF (http://www.bibliotecas.uff.br). 

Esses acervos estão em dois arquivos, disponíveis na pasta *data*. Seus nomes são *acervo-cefetrj.csv* e *acervo-uff.xlsx*.

Para executar a funcionalidade de importação de um acervo bibliográfico, o ColetaISBN disponibiliza o *script* *importar_acervo.py*. Esse script disponibiliza algumas opções de linha de comando, descrita a seguir.

    - -i nome_arq: permite especificar o nome do arquivo de entrada (contendo acervo a ser importado), no formato csv ou xlsx.
    - -v: modo 'verboso' de execução do script (para fins de depuração e entendimento do seu funcionamento.
    - -isbn col: especifica nome da coluna relativa ao ISBN no arquivo de entrada. Essa opção é necessário, posto que diferente bibliotecas possuem diferentes esquemas de armazenamento de seus acervos e portanto diferentes nomes de colunas na tabela correspondente a livros. Por exemplo, no acervo do CEFET/RJ a coluna que armazena o ISBN é denominada ISBN_ISSN, enquanto que no acervo da UFF essa coluna é denominada ESCALA.
  - -fonte cols: argumento que permite ao usuário especificar os nomes de colunas a importar do acervo bibliotecário.
  - -destino cols: argumento que permite ao usuário especificar os nomes de colunas correspondentes na base unificada

Exemplos de uso do script importar_acervo.py são fornecidos a seguir. O efeito de execução desses dois comandos é a integração dos acervos de livros da UFF e do cEFET/RJ à base unificada do ColetaISBN. 

```
python importar_acervo.py -i acervo-uff.xlsx 
    -isbn ESCALA 
    -json -fonte TITULO,DESC_AREA_CONHECIMENTO,
    AUTOR,ESCALA,PUBLICACAO,EDICAO,PAGINA 
    -destino titulo,assuntos,autores,isbn13,editora,
    edicao,qtd_paginas
```

```
python importar_acervo.py -i acervo-cefetrj.csv 
    -isbn ISBN_ISSN 
    -json -fonte TITULO,ASSUNTOS,AUTORES,IDIOMA,
    ISBN_ISSN,EDITORA
    -destino titulo,assuntos,autores,idioma,isbn13,
    editora
```

Uma aspecto importante desta funcionalidades diz respeito à validação e normalização dos dados armazenados na coluna de ISBN existente no arquivo a ser importado. Por exemplo, nos acervos aos quais tivemos acesso, existem entradas sem ISBN, com ISBN inválido, ou com valores como por exemplo "9780765804136 (v.1).", " 8573350563 (obra completa).", " 8572280189 .", entre outros. Em nossa solução, tomamos a decisão de normalizar os valores de ISBN para armazenar na base unificada do ColetaISBN. Em particular, utilizamos a biblioteca Python denominada isbnlib para realizar a normalização desses valores e para converter eventuais códigos de ISBN10 para ISBN13.

Outro aspecto importante dessa funcionalidade é que ela contempla a integração de esquemas. Por exemplo, no acervo do CEFET/RJ, não há a informação de quantidade de páginas de cada livro, mas no acervo da UFF essa informação existem. Em nossa solução, quando importamos um novo acervo é existe livro na base unificada que podem ter sua informação completada, o script realiza essa tarefa.

### Detecção de nomes de autores e de editoras semelhantes

A ideia que implementamos nesta funcionalidade foi a seguinte. Muitas vezes, uma mesma obra é cadastrada de formas diferente. Por exemplo, um autor cujo nome José Silva pode ser sido cadastrado como "José Silva", "Silva, José" e "J. Silva". Essa funcionalidade permite detectar duas ou mais entradas na base unificada que provavelmente correspondem à mesma entidade. Essa funcionalidade pode ser aplicada a diversos campos, como por exemplo, nomes autores e nomes de editoras. 

A funcionalidade descrita acima está implementada no script denominada search_duplicates.py. Um exemplo de execução desse script é fornecido a seguir. Neste exemplo, a opção -i permite especificar o nome do arquivo contendo o acervo bibliográfico, enquanto que a opção -col permite especifica o nome da coluna sobre a qual realizar a análise. Esse script produz como resultado de sua execução um arquivo CSV contendo as posições das duplicatas.

```
python search_duplicates.py -i file_name -col autores 
```

Implementamos essa funcionalidade por meio do uso da biblioteca Python denominada dysamby (https://pypi.org/project/disamby/). De acordo com os seus desenvolvedores, disamby é um pacote escrito puramente em Python e projetado para realizar a desambiguação da entidades com base na correspondência difusa (*fuzzy matching*} de cadeias de caracteres.

Entendemos que essa funcionalidade é útil para eventuais curadorias na base unificada: se duas ou mais entradas fazem referência a uma mesma entidade por meio de nomes distintos, essas entradas poderiam ser modificadas para armazenar um nome canônico para a entidade em questão. Essa funcionalidade também é útil para o contexto específico da Plataforma Sucupira, visto que nela é preciso atrelar os autores a um determinado livro.

### Obtenção de entradas a partir de APIs online

A terceira funcionalidade que implementamos no ColetaISBN foi a que possibilita a recuperação de informação dos metadados e dados acerca de um livro a partir de alguma API online (Web service). Para isso, mais uma vez, utilizamos a biblioteca Python isbnlib. Implementamos essa funcionalidade no script de nome recupera_livro.py. Nesse script, a opção -s permite ao usuário especificar a API online a ser consultada. As opções -isbn e -isbns são exclusivas entre si. A primeira permite fornecer um único ISBN para realizar a recuperação (busca). Já a segunda permite fornece uma lista de ISBNs em um arquivo txt. Um exemplo de uso deste script é fornecido abaixo. 

```
python recupera_livro.py -isbn 9780446310789 -s openl
```

```
python recupera_livro.py -isbns isbns.txt -s openl
```

Um melhoramento que pretendemos realizar no futuro é integrar essa funcionalidade com a de importação de dados. Dessa forma, a base unificada do ColetaISBN poderia evoluir para conter dados recuperados por este script.
