# desafio-capes-livros

Nesse desafio, iremos tentar importar dados de 3 diferentes bases de dados: Googlebooks, Open library e Crossref. Além disso, organizar alguns dados do cefet e da uff.

## Modo de uso:

Primeiro clone esse repositorio. A busca pelos dados será feita por linha de comando.

### Exemplos:

Para fazer uma busca com os dados do googlebooks, digite:

>python requisicao_dados.py -l gbooks -i 0596007973

-l é a bilioteca a ser usada, podendo ser gbooks, openl ou crossref
-i é um numero isbn
O resultado é um arquivo json, que ficará guardado na pasta jsonfiles. Para mostrar esse arquivo digite:

>python -m json.tool json_0596007973.json



