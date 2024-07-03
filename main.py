from scipy.stats import shapiro
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('Drugs.csv')

#questao(1)
#nota: melhorar código, da pra resumir bastante
porc_dados_faltando = df.isnull().sum()/len(df['ID'])*100
print(porc_dados_faltando)

porc_dados_faltando.plot(kind = "bar", title = "PORCENTAGEM DE DADOS FALTANDO" , xlabel = "DADOS", ylabel = "PORCENTAGEM", figsize= (12,10))
plt.savefig('dados_faltando.png')
plt.clf()

#I)preenchimento dos dados qualitativos a partir da moda

def preencher_com_moda(dataframe, coluna): #funcao para pegar as colunas e preencher com a moda os dados faltando, já que faltam pouquíssimos dados o uso da moda é adequado
    moda = dataframe[coluna].mode()[0]
    dataframe[coluna] = dataframe[coluna].fillna(moda)
    return dataframe

preencher_com_moda(df, "Gender");  preencher_com_moda(df, "Education");  preencher_com_moda(df, "Country");  preencher_com_moda(df, "Ethnicity"); 
preencher_com_moda(df, "Alcohol");  preencher_com_moda(df, "Amphet");  preencher_com_moda(df, "Amyl");  preencher_com_moda(df, "Benzos");
preencher_com_moda(df, "Caff");  preencher_com_moda(df, "Cannabis"),  preencher_com_moda(df, "Choc");  preencher_com_moda(df, "Coke");  preencher_com_moda(df, "Crack")

#II)preenchimento dos dados quantitativos

#1) preencher income com as rendas médias dos paises(exceção: others, que será a a média mundial)fontes : https://www.worlddata.info/average-income.php e https://www.zippia.com/advice/average-income-worldwide/

renda_media_UK = 4103;  renda_media_USA = 6397.5;  renda_media_CAN = 4442.5;  renda_media_AUS = 5070;
renda_media_IRE = 6644.1;  renda_media_NEW = 4090.3;  renda_media_OTH = 811

df.loc[(df['Country'] == "UK") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "UK", 'Income (USD)'].fillna(renda_media_UK)
df.loc[(df['Country'] == "USA") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "USA", 'Income (USD)'].fillna(renda_media_USA)
df.loc[(df['Country'] == "Canada") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "Canada", 'Income (USD)'].fillna(renda_media_CAN)
df.loc[(df['Country'] == "Australia") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "Australia", 'Income (USD)'].fillna(renda_media_AUS)
df.loc[(df['Country'] == "Republic of Ireland") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "Republic of Ireland", 'Income (USD)'].fillna(renda_media_IRE)
df.loc[(df['Country'] == "EUA") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "EUA", 'Income (USD)'].fillna(renda_media_USA)
df.loc[(df['Country'] == "New Zealand") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "New Zealand", 'Income (USD)'].fillna(renda_media_NEW)
df.loc[(df['Country'] == "Other") & (df['Income (USD)'].isnull()), 'Income (USD)'] = df.loc[df['Country'] == "Other", 'Income (USD)'].fillna(renda_media_OTH)

#2) preencher Nscore, Escore, Oscore, ... com a média
#   ao analisar a descrição dessas características com o describe() e a distribuição com o value_counts() , nota-se que não há grandes outliers, portanto usar a média é a melhor opção para preencher os dados restantes

df.loc[df['Nscore'].isnull(), 'Nscore'] = df['Nscore'].mean();  df.loc[df['Escore'].isnull(), 'Escore'] = df['Escore'].mean()
df.loc[df['Oscore'].isnull(), 'Oscore'] = df['Oscore'].mean();  df.loc[df['AScore'].isnull(), 'AScore'] = df['AScore'].mean()
df.loc[df['Cscore'].isnull(), 'Cscore'] = df['Cscore'].mean();  df.loc[df['SS'].isnull(), 'SS'] = df['SS'].mean()

df['Impulsive'] = pd.to_numeric(df['Impulsive'], errors='coerce'); df.loc[df['Impulsive'].isnull(), 'Impulsive'] = df['Impulsive'].mean()

porc_dados_faltando = df.isnull().sum()/len(df['ID'])*100
print(porc_dados_faltando)

#questao (2) (3) (4) (10) (12) e (13)

# grafico de distribuição de idade na amostra
df['Age'].value_counts().plot(kind = "bar", title = "DISTRIBUIÇÃO DAS IDADES" , xlabel = "FAIXA ETÁRIA", ylabel = "QUANTIDADE")
plt.savefig('distribuicaoidades.png')
plt.clf()

# funcao para pegar umca coluna e uma droga(exemplo: Gênero e Álcool) e calcular a média de consumo dessa coluna no dataframe
def analise_coluna_droga(dataframe, coluna, drogas):

    lista_analise = [] #lista utilizada para criar dataframe do gráfico, o qual receberá listas no formato [coluna, media, droga]

    for droga in drogas:
        print("--------------------", droga , "--------------------")

        #separação das médias e de cada string única na coluna a ser analisada
        valores_unicos = sorted(dataframe[coluna].unique(), key = lambda x: str(x)) 
        medias = []
        media_total = 0

        for val in valores_unicos:

            dfval = dataframe.loc[(df[coluna] == val), [coluna, droga]] #dataframe somente com a coluna e o consumo da droga(ex: dataframe com as colunas'Gender' e 'Alcohol')
            totalval = dataframe.loc[(df[coluna] == val), coluna].count() #total de pessoas nessa coluna(ex: total de pessoas do genero feminino)

            media = 0

            # escala de 0 a 6 para medir média de consumo da característica analisada
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

            media = media/totalval #como calculamos o 'totalval' baseado em cada valor único(ex: 'F' em 'Gender'), não há risco de divisão por zero
            medias.append(media) #adicionamos a media aqui para calcular a media de todos os 'val' únicos na 'media_total'

            print(f"A MEDIA DE CONSUMO DE {val} é {media:.2f}\n" )

            lista_analise.append([val, media, droga])
        
        for val in medias:
            media_total += val/len(medias) #se len(medias) for zero o loop nem é executado já que é 'for val in medias', logo sem risco de divisão por zero

        print(f"MEDIA FINAL: {media_total:.2f}\n")

    df_grafico = pd.DataFrame(lista_analise, columns = [coluna, 'Média', 'Droga'])
    sns.barplot(data = df_grafico, x = 'Droga', y = 'Média', hue = coluna)
    sns.title(f"Gráfico de consumo baseado na {coluna}")
    plt.savefig(f"grafico_consumo_por_{coluna}.png")
    plt.clf()
    #grafico final da análise



drogas = ['Alcohol', 'Amphet', 'Amyl', 'Benzos', 'Caff', 'Cannabis', 'Choc', 'Coke', 'Crack', 'Ecstasy', 'Heroin', 'Ketamine', 'Legalh', 'LSD', 'Meth', 'Mushrooms', 'Nicotine' ,'Semer', 'VSA']
drogas_alucinogenas = ['LSD', 'Ecstasy', 'Ketamine', 'Cannabis' , 'Mushrooms']
drogas_ilicitas = ['Amphet', 'Amyl', 'Coke', 'Crack', 'Ecstasy', 'Heroin', 'Ketamine', 'Legalh', 'LSD', 'Meth', 'Mushrooms'] #de acordo com a legislação brasileira

#analise para questao 2
analise_coluna_droga(df, 'Age', drogas)

#analise para questao 3
analise_coluna_droga(df, 'Education', drogas)

#analise para questao 4 
analise_coluna_droga(df, 'Gender', drogas_alucinogenas)

 #analise para questao 10
analise_coluna_droga(df, 'Education', drogas_ilicitas)

#analise para questao 13
analise_coluna_droga(df, 'Country', drogas)

# questao  
