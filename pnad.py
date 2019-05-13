import pandas as pd
import numpy as np
import scipy.stats as scs


def teste_chi2(df, campo_analise):
    dados = df[['internet_via_celular', campo_analise]].dropna()
    categorias = list(dados[campo_analise].unique()) # Vê a quantidade de valores distintos no campo
    n_categorias = len(categorias)

    # Faz a contagem de pessoas com internet e sem internet dependendo de sua categoria
    tem_internet = dados[dados['internet_via_celular'] == 1]
    nao_tem_internet = dados[dados['internet_via_celular'] == 0]
    tabela_tem_internet = []
    tabela_nao_tem_internet = []
    total_categoria = []
    for categoria in categorias:
        tabela_tem_internet.append(len(tem_internet[tem_internet[campo_analise] == categoria]))
        tabela_nao_tem_internet.append(len(nao_tem_internet[nao_tem_internet[campo_analise] == categoria]))

    count = 0
    for i in tabela_tem_internet:
        count = count + i
    tabela_tem_internet.append(count)


    count = 0
    for i in tabela_nao_tem_internet:
        count = count + i
    tabela_nao_tem_internet.append(count)

    for i in range(0, n_categorias+1):
        total_categoria.append(tabela_tem_internet[i] + tabela_nao_tem_internet[i])

    tabela = np.array([tabela_tem_internet, tabela_nao_tem_internet, total_categoria])

    # Cria matriz de probabilidade
    probabilidades = np.zeros((3,n_categorias+1))
    for i in range(0, n_categorias+1):
        probabilidades[0][i] = tabela[0][i]/tabela[2][i]
        probabilidades[1][i] = tabela[1][i]/tabela[2][i]
        probabilidades[2][i] = 1

    # Cria matriz de valores esperados de acordo com a probabilidade global de ter ou não internet
    # de acordo com a categoria.
    esperado = np.zeros((2, n_categorias))
    for i in range(0, 2):
        for j in range(n_categorias):
            esperado[i][j] = tabela[2][j] * probabilidades[i][n_categorias]

    # qui = 0
    # for i in range(0,2):
    #     for j in range((n_categorias)):
    #         qui = qui + pow((tabela[i][j] - esperado[i][j]),2)/esperado[i][j]
    # print()
    # print("Analisando %s" % campo_analise)
    # print("--------------")
    # # print()
    # # print("Qui²: %f" % qui)
    # print()
    # tabela = np.array([tabela[0][:-1], tabela[1][:-1]])
    # print("Tabela para análise")
    # print(categorias)
    # print(tabela)
    # print()
    # print("Tabela esperada")
    # print(categorias)
    # print(np.ceil(esperado))
    # erro = esperado
    # for i in range(0,2):
    #     for j in range(0, n_categorias):
    #         erro[i][j] = abs(1-tabela[i][j]/esperado[i][j])
    # print()
    # print("Probabilidade")
    # print(categorias)
    # print(probabilidades)
    # print()
    # print("Diferença entre dados base e dados esperados")
    # print(categorias)
    # print(erro)

    # print()
    # print("Diferença média:")
    # print(np.mean(erro))
    return probabilidades
    # print(scs.chi2_contingency(tabela))

df = pd.read_csv(r'./pnad.csv')
# prob = teste_chi2(df, 'nivel_de_instrucao')
# com_internet = df[df['internet_via_celular'] == 1]
# print()
# print("Percentual de pessoas com conexão à internet via celular no Brasil: %f" % (len(com_internet)/len(df)))

idade = int(input("Informe a idade: "))
print()

alfabetizado = int(input("Informe se é alfabetizado (0-Não / 1-Sim): "))
print()

print("Anos de estudo")
print("0- 11 a 14 anos")
print("1- 1 a 3 anos")
print("2- Sem instrucao e menos de 1 ano")
print("3- 4 a 7 anos")
print("4- 8 a 10 anos")
print("5- 15 anos ou mais")
print("6- Nao determinados")
anos_estudo = int(input("Digite de acordo com os anos de estudo: "))
print()

print("Nível de instrução")
print("0- Medio completo ou equivalente")
print("1- Superior incompleto ou equivalente")
print("2- Superior completo")
print("3- Fundamental incompleto ou equivalente")
print("4- Sem instrucao")
print("5- Fundamental completo ou equivalente")
print("6- Medio incompleto ou equivalente")
print("7- Nao determinado")
nivel_instrucao = int(input("Digite de acordo com o nivel de instrução: "))
print()

at_agricola = int(input("Informe se possui atividade agrícola (0-Não / 1-Sim): "))
print()

prob_idade = teste_chi2(df, "idade")
prob_alf  = teste_chi2(df, "alfabetizado")
prob_ae = teste_chi2(df, "anos_de_estudo")
prob_ni = teste_chi2(df, "nivel_de_instrucao")
prob_aa = teste_chi2(df, "atividade_agricola")

cat_idade = list(df["idade"].unique())
index = cat_idade.index(idade)
prob = np.mean([prob_idade[0][index], prob_alf[0][alfabetizado], prob_ae[0][anos_estudo], prob_ni[0][nivel_instrucao], prob_aa[0][at_agricola]])
print("Chance de possuir conexão com internet via celular: %d %%" % (prob*100))

