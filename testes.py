
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# read_csv(caminho_para_o_documento) -> le o decumento .csv 
# df['Nome da coluna'] -> acessa a coluna, é possível realizar operações com a coluna de forma que ela cria um df separado com os valores true, false
# df.info(), df.shape() -> fornece o total de elementos do df, colunas,...
# df.loc(INDEX, COLUMNS) -> dado um index ou um booleano(df['Coluna'] == ...), ele fornece os dados da linha(série)
# df.max() -> fornece os maiores dados por coluna de todo o data frame
# df.describe() -> fornece o valor máximo, média, mínimo, ...
# df.sort_values(by=['Coluna'], ascending = False/True) -> arruma a coluna de forma decrescente
# df['Nome da coluna'].value_counts() -> mostra quantas vezes aparece certo valor naquela coluna
# df.sample -> amostragem aleatória de dados do dataframe
# df.query -> fornece os dados a partir de uma string booleana(ao utilizar expressões com um espaço entre elas é preciso usar `` e variáveis o @)
# df['Coluna'].value_counts() -> mostra a quantidade de valores de cada tipo diferente(aceita sort como parametro)
# df['Coluna'].isin() -> retorna se os valores da coluna estao dentro de uma lista de parametros do isin()
# df['Coluna].quantile(.x) -> retorna o valor minimo para chegar nos top x% da coluna


df = pd.read_csv('Drugs.csv')
df.head()


