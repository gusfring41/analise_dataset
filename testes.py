from scipy.stats import shapiro
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

# funcao para pegar umca coluna e uma droga(exemplo: Gênero e Álcool) e calcular a média de consumo dessa coluna no dataframe
def analise_coluna_droga(dataframe, coluna, droga):
    valores_unicos = sorted(dataframe[coluna].unique(), key = lambda x: str(x))
    media = 0
    for val in valores_unicos:

        dfval = df.loc[(df[coluna] == val), [coluna, droga]]
        totalval = df.loc[(df[coluna] == val), coluna].count()

        media = 0

        totalval_6 = dfval.loc[dfval[droga] == "CL6"].shape[0]
        media += totalval_6*6
        totalval_5 = dfval.loc[dfval[droga] == "CL5"].shape[0]
        media += totalval_5*5
        totalval_4 = dfval.loc[dfval[droga] == "CL4"].shape[0]
        media += totalval_4*4
        totalval_3 = dfval.loc[dfval[droga] == "CL3"].shape[0]
        media += totalval_3*3
        totalval_2 = dfval.loc[dfval[droga] == "CL2"].shape[0]
        media += totalval_2*2
        totalval_1 = dfval.loc[dfval[droga] == "CL1"].shape[0]
        media += totalval_1*1

        media = media/totalval
        print(f"A MEDIA DE CONSUMO DE {val} é {media:.2f}%" )

analise_coluna_droga(df, 'Gender', 'Alcohol')















