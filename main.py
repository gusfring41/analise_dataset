from scipy.stats import shapiro
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Drugs.csv')

print(df)

faltantes = df.isnull().sum()
print(faltantes)

faltantes_percentual = (df.isnull().sum()/ len(df['ID']))*100
print(faltantes_percentual)

df['Income (USD)'] = df['Income (USD)'].fillna(1000) #preenche os salários com o valor de 1000 dolares

for x in range(33): #loop para verificar se os dados tem uma distribuição normal ou anormal
    
    coluna_analisada = df.iloc[:, x]
    faltaDados = coluna_analisada.isnull()

    if(faltaDados):
        coeficiente = shapiro(coluna_analisada)
        if(coeficiente > 0.05):
            print("MEDIA")
        else:
            print("MEDIANA")
