# %%
import pandas as pd


# Introduza o nome da variável, ou colunas, e quantos bits. (0 a n).
var = 'X'

ativar = True
l_colunas = ['LD', 'CLR', 'X', 'Q', 'Q*', 'Te']


# %%

print('\nGERADOR DE TABELAS VERDADES')
while True:
    try:
        n = int(input('\nNº de entradas: ')) -1
        escolha = input('Deseja colocar nomes para cada coluna?(y/n) ')
        if escolha == 'y':
            ativar = True
            l_colunas = [x for x in input('Escreva os nomes separados por espaços:\n').split()]
            l_l_alto = []
            l_l_donc = []
            print(f'Digite os números decimais, separados por espaços, em que a saída é ativa (1) max ({2**(n+1)-1}).')
            for key in l_colunas[n+1:]:
                l_temp = sorted([int(x) for x in input(f'{key}: ').split()])
                
                l_l_alto.append(l_temp)
            print('\nMesmo processo, agora com don\'t care ( - ).')
            for key in l_colunas[n+1:]:
                l_temp = sorted([int(x) for x in input(f'{key}: ').split()])
                l_l_donc.append(l_temp)
        else:
            ativar = False
        break
    except:
        print('Digite um valor válido.')


# %%
# Gerar número total de linhas
l = []
for colunas in range(2**(n+1)):
    l.append(0)

# dataframe
dic = {f'{var}{n}': l}
df = pd.DataFrame(dic)


# %%
# Loop para adicionar todos os Xn
for colunas in range(n, -1, -1):
    for loops in range(2**(n-colunas)):

        if loops == 0:
            df.loc[0:2**colunas-1, f'{var}{colunas}'] = 0
            df.loc[2**colunas : 2**(colunas+1)-1, f'{var}{colunas}'] = 1
        else:
            df.loc[2**(colunas+1)*loops : 2**(colunas+1)*loops + 2**colunas-1, f'{var}{colunas}'] = 0
            df.loc[2**(colunas+1)*loops + 2**colunas:, f'{var}{colunas}'] = 1

# Mudando tipo de valores para inteiros
df = df.apply(lambda columns: columns.astype(int))

# Lista de counas
l_xn = df.columns.tolist()

# %% [markdown]
# # Extra
# 

# %%
# Renomear colunas ao gosto
if ativar == True:
    for antes, depois in zip(l_xn, l_colunas):
        df.rename(columns={antes:depois}, inplace=True)


# %%
# Extra 
# l_l_alto = [[1, 3, 10, 11], [0, 1]]
# l_l_donc = [[12, 13, 14, 15], [1, 6, 7]]
if ativar == True:
    # Dicionário de resultados em index altos
    d_index_altos = {}

    for key, l_i in zip(l_colunas[n+1:], l_l_alto):
        l_temp = []
        for index in df.index.tolist():
            if index not in l_i:
                l_temp.append(0)
            else:
                l_temp.append(1)

        d_index_altos[key] = l_temp
        df_temp = pd.DataFrame(d_index_altos)
    df = pd.concat([df, df_temp], axis=1)


    # Adicionar don't cares
    l_temp = []
    for key, l_i in zip(l_colunas[n+1:], l_l_donc):
        for j in l_i:
            df.loc[j,key] = '-'

df.to_excel('Output.xlsx')


