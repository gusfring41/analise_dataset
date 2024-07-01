from scipy.stats import shapiro
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Drugs.csv')

#questao(1)

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

#questao(2)

# grafico de distribuição de idade na amostra
df['Age'].value_counts().plot(kind = "bar", title = "DISTRIBUIÇÃO DAS IDADES" , xlabel = "FAIXA ETÁRIA", ylabel = "QUANTIDADE")
plt.savefig('distribuicaoidades.png')
plt.clf()

# analise da o consumo da droga feita pela porcentagem de consumo de cada faixa_etária para determinar qual faixa-etária usa mais
def analise_consumo(dataframe, droga):

    nome_droga = droga
    print("\n---------------------------------", droga, "---------------------------------\n")

    total_idade = df['Age'].value_counts().sort_index() 

    lista_pares_das_porcentagens_CL6 = []
    lista_pares_das_porcentagens_CL5 = []
    lista_pares_das_porcentagens_CL4 = []

    idades_unicas = sorted(df['Age'].unique(), key=lambda x: str(x))  # pego as faixas_etárias únicas como strings

    for idade in idades_unicas:  # para cada idade única, eu calcúlo a porcentagem de usuários CL6, CL5 e CL4 daquela droga e armazeno na lista como um par(porcentagem, "faixa-etária")

        max_idade = df.loc[(df[droga] == 'CL6') & (df['Age'] == idade), 'Age'].count()
        max_idade2 = df.loc[(df[droga] == 'CL5') & (df['Age'] == idade), 'Age'].count()
        max_idade3 = df.loc[(df[droga] == 'CL4') & (df['Age'] == idade), 'Age'].count()

        total_pessoas_idade = total_idade.get(idade, 1) 

        porcentagem = (max_idade / total_pessoas_idade) * 100
        porcentagem2 = (max_idade2 / total_pessoas_idade) * 100
        porcentagem3 = (max_idade3 / total_pessoas_idade) * 100

        lista_pares_das_porcentagens_CL6.append((porcentagem, idade))
        lista_pares_das_porcentagens_CL5.append((porcentagem2, idade))
        lista_pares_das_porcentagens_CL4.append((porcentagem3, idade))
    
    media_porcentagem_CL6 = 0; media_porcentagem_CL5 = 0; media_porcentagem_CL4 = 0

    for i in range(6):
        porcentagem1, idade1 = lista_pares_das_porcentagens_CL6[i]; porcentagem2, idade2 = lista_pares_das_porcentagens_CL5[i]; porcentagem3, idade3 = lista_pares_das_porcentagens_CL4[i]
        media_porcentagem_CL6 += porcentagem1/6
        media_porcentagem_CL5 += porcentagem2/6
        media_porcentagem_CL4 += porcentagem3/6

    print("CL6: ")  # mostro as idades com mais consumidores percentuais CL6
    lista_pares_das_porcentagens_CL6.sort(reverse = True, key=lambda x: x[0])
    porcentagem_1, idade_1 = lista_pares_das_porcentagens_CL6[0]
    porcentagem_2, idade_2 = lista_pares_das_porcentagens_CL6[1]
    print(f"1) Idade: {idade_1}, Porcentagem: {porcentagem_1:.2f}% 2) Idade: {idade_2}, Porcentagem: {porcentagem_2:.2f}% Média: {media_porcentagem_CL6:.2f}%")

    print("CL5: ")  # mostro as idades com mais consumidores percentuais CL5
    lista_pares_das_porcentagens_CL5.sort(reverse = True, key=lambda x: x[0])
    porcentagem_1, idade_1 = lista_pares_das_porcentagens_CL5[0]
    porcentagem_2, idade_2 = lista_pares_das_porcentagens_CL5[1]
    print(f"1) Idade: {idade_1}, Porcentagem: {porcentagem_1:.2f}% 2) Idade: {idade_2}, Porcentagem: {porcentagem_2:.2f}%  Média: {media_porcentagem_CL5:.2f}%")

    print("CL4: ")  # mostro as idades com mais consumidores percentuais CL4
    lista_pares_das_porcentagens_CL4.sort(reverse = True, key=lambda x: x[0])
    porcentagem, idade = lista_pares_das_porcentagens_CL4[0]
    porcentagem_2, idade_2 = lista_pares_das_porcentagens_CL4[1]
    print(f"1) Idade: {idade}, Porcentagem: {porcentagem:.2f}% 2) Idade: {idade_2}, Porcentagem: {porcentagem_2:.2f}% Média: {media_porcentagem_CL4:.2f}%")

    # a partir da maior quantidade de usuários CL6, CL5 e CL4 e da média eu concluo se há uma grande diferença de consumo entre as faixas-etárias e, se houver, eu crio um gráfico para analisar melhor
    return 

analise_consumo(df, 'Alcohol');analise_consumo(df, 'Amphet');analise_consumo(df, 'Benzos');analise_consumo(df, 'Caff');analise_consumo(df, 'Cannabis');
analise_consumo(df, 'Choc');analise_consumo(df, 'Coke');analise_consumo(df, 'Crack');analise_consumo(df, 'Ecstasy');analise_consumo(df, 'Heroin');
analise_consumo(df, 'Ketamine');analise_consumo(df, 'Legalh');analise_consumo(df, 'LSD');analise_consumo(df, 'Meth');analise_consumo(df, 'Mushrooms');
analise_consumo(df, 'Semer');analise_consumo(df, 'VSA')

dataframe_sorted = df.sort_values(by = 'Cannabis', ascending = False)  # grtáfico de uso da cannabis
imagem = sns.violinplot(data = dataframe_sorted, x = 'Age', y = 'Cannabis')
plt.tight_layout()
plt.xlabel('Faixa Etária')
plt.ylabel('Quantidade de Pessoas CLX')
plt.savefig("consumoporidadecannabis.png")
plt.clf()

dataframe_sorted = df.sort_values(by = 'Caff', ascending = False)   # gráfico de uso da cafeína
imagem = sns.violinplot(data = dataframe_sorted, x = 'Age', y = 'Caff')
plt.tight_layout()
plt.xlabel('Faixa Etária')
plt.ylabel('Quantidade de Pessoas CLX')
plt.savefig("consumoporidadecafe.png")
plt.clf()

#questao (3)

#questao (4)

# funcao para pegar umca coluna e uma droga(exemplo: Gênero e Álcool) e calcular a média de consumo dessa coluna no dataframe
def analise_coluna_droga(dataframe, coluna, droga):

    print("--------------------", droga , "--------------------")

    valores_unicos = sorted(dataframe[coluna].unique(), key = lambda x: str(x))
    media = 0
    for val in valores_unicos:

        dfval = df.loc[(df[coluna] == val), [coluna, droga]]
        totalval = df.loc[(df[coluna] == val), coluna].count()

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

        media = media/totalval
        print(f"A MEDIA DE CONSUMO DE {val} é {media:.2f}\n" )

drogas_alucinogenas = ['LSD', 'Ecstasy', 'Ketamine', 'Cannabis' , 'Mushrooms']
for droga in drogas_alucinogenas:
    analise_coluna_droga(df, 'Gender', droga)
