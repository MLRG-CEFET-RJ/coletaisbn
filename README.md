# desafio-capes-livros

Nesse desafio iremos tentar buscar dados isbn como autores,titulo,obra,etc... e formatar tudo em um arquivo json ou xml.

## Modo de uso:

A busca pelos dados consiste em duas classes. <br />
A primeira busca pode ser feita com dados de universidades como CEFET,UFF,etc. Para utilizar essa busca, é necessario que os dados estejam no formato csv ou xlsx. Note que os dados no formato csv possibilitam uma busca visivelmente mais rapida que dados no formato xlsx. O resultado dessa classe irá gerar uma lista com numeros isbn para que a segunda busca também possa ser possível.<br />
A segunda busca pode ser feita na nuvem, com bibliotecas como googlebooks, openlibrary ou crossref. Note que para utilizar essa busca é necessario uma lista com numeros isbn.

### Exemplos:

Para fazer uma busca com os dados de universidades, primeiro coloque os arquivos na pasta Acervos:
![Capturar1](https://user-images.githubusercontent.com/39687418/62415606-f3eb8880-b602-11e9-8a95-6fa2d6dfb344.PNG)
![Capturar](https://user-images.githubusercontent.com/39687418/62415607-fc43c380-b602-11e9-981f-c2b65ea27dc7.PNG)
![Capturar2](https://user-images.githubusercontent.com/39687418/62415608-fea61d80-b602-11e9-80dd-2dca47c4fe55.PNG)

Aqui podemos ver que temos dois arquivos, acervo-cefetrj.csv e acervo-uff.xlsx<br/>
Podemos prosseguir então, para ver o conteudo desses acervos. Para ver quais são as colunas dos arquivos, basta escrever:
![Capturar3](https://user-images.githubusercontent.com/39687418/62415609-006fe100-b603-11e9-8253-90a7ea299b69.PNG)
![Capturar4](https://user-images.githubusercontent.com/39687418/62415611-02d23b00-b603-11e9-8747-fe25565966b4.PNG)
![Capturar12](https://user-images.githubusercontent.com/39687418/62415623-15e50b00-b603-11e9-8753-8ee79d272f82.PNG)
![Capturar13](https://user-images.githubusercontent.com/39687418/62415624-17aece80-b603-11e9-9bff-f8ec3a8b2309.PNG)

Pronto. Agora que sabemos quais são as colunas dos arquivos, podemos inspecionar o que tem dentro dessas colunas para determinar se queremos ou não por essas colunas no nosso futuro arquivo json ou xml. Para inspecionar o que tem dentro das colunas, você pode escrever:
![Capturar5](https://user-images.githubusercontent.com/39687418/62415613-05cd2b80-b603-11e9-97fa-31e839be2d2f.PNG)
![Capturar6](https://user-images.githubusercontent.com/39687418/62415615-0796ef00-b603-11e9-9307-920edcf6a03b.PNG)

Note que essa etapa é importante, pois só podemos continuar com as próximas etapas após termos determinado qual dessas colunas contem os numeros isbn. Isso pode ser um pouco difícil, pois nem sempre é claro quais dessas colunas contém os numeros ISBN. No dataset da UFF por exemplo, os números ISBN ficam dentro da coluna ESCALA.
![Capturar15](https://user-images.githubusercontent.com/39687418/62415728-fe0e8680-b604-11e9-829e-0742477bb961.PNG)
![Capturar16](https://user-images.githubusercontent.com/39687418/62415731-0070e080-b605-11e9-8aee-b63162b1fc35.PNG)

Agora que já sabemos qual coluna contém os números ISBN, precisamos gerar a lista com os números ISBN. Isso é essencial e precisa ser feito para que o restante do código possa funcionar. Essa etapa é necessária porque a chave que iremos usar para criar o arquivo JSON são os números ISBN. Como nem todas as linhas das planilhas do CEFET e da UFF contém um número ISBN, esse comando irá reduzir o arquivo csv ou xlsx para um novo arquivo, que terá todas as linhas sem números ISBN removidas do arquivo principal.
![Capturar7](https://user-images.githubusercontent.com/39687418/62415616-08c81c00-b603-11e9-887d-ddfd135c2caa.PNG)
![Capturar19](https://user-images.githubusercontent.com/39687418/62415831-76c21280-b606-11e9-9a14-f0c0a8bd1266.PNG)

A próxima etapa consiste em gerar os arquivos xml ou json. O comando que faz isso possibilita que você escolha quais colunas da planilha deseja adicionar ao arquivo json ou xml. Note que o comando -json irá gerar apenas um arquivo json, enquanto que o comando -xml irá gerar ambos.
![Capturar8](https://user-images.githubusercontent.com/39687418/62415617-0c5ba300-b603-11e9-9d80-d0ab11c7c743.PNG)
![Capturar9](https://user-images.githubusercontent.com/39687418/62415618-0e256680-b603-11e9-81e4-f3dc33ff42bd.PNG)
![Capturar17](https://user-images.githubusercontent.com/39687418/62415733-01a20d80-b605-11e9-9584-0f0eed35fcca.PNG)
![Capturar18](https://user-images.githubusercontent.com/39687418/62415735-036bd100-b605-11e9-88d5-54ba41e01689.PNG)

Comandos úteis:








