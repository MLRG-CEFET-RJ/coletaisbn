# desafio-capes-livros

Nesse desafio, iremos tentar importar dados de 3 diferentes bases de dados: Googlebooks, Open library e Crossref. Além disso, organizar alguns dados do cefet e da uff.

## Modo de uso:

Primeiro clone esse repositorio. A busca pelos dados será feita por linha de comando.

### Exemplos:

Para fazer uma busca com os dados do googlebooks, digite:

>python requisicao_dados.py -l gbooks -i 0596007973

-l é a bilioteca a ser usada, podendo ser gbooks, openl ou crossref<br />
-i é um numero isbn<br />
O resultado é um arquivo json, que ficará guardado na pasta jsonfiles. Para mostrar esse arquivo digite:

>python -m json.tool json_0596007973.json

De maneira similar também é possivel fazer uma busca com uma lista de numeros isbn.<br />
Obs: Para esse comando funcionar, a lista precisa ser do formato txt ou csv e conter um numero isbn em cada linha

>python requisicao_dados.py -l gbooks -f my_list.txt

O resultado é um arquivo json com todos os dados dos numeros isbn

>python -m json.tool json_my_list.json






