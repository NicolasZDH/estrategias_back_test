import numpy as np
import pandas as pd
import random
from fundo_quanti.back_test import back_test
from fundo_quanti.prospect_strategy import prospect_theory as pt
from fundo_quanti.dados_yahoo_finance import shares as sh
import warnings
import time

warnings.filterwarnings("ignore")


# Sinta-se livre para brincar com os valores abaixo

CHANCE_MUT = .40      # Chance de mutação de um peso qualquer
CHANCE_CO = .25      # Chance de crossing over de um peso qualquer
NUM_INDIVIDUOS = 15  # Tamanho da população
NUM_MELHORES = 1     # Número de indivíduos que são mantidos de uma geração para a próxima
TICKET = ["AZUL4.SA"]
sh_objct = sh('2016-01-01', '2018-12-31', TICKET)
SHARES = sh_objct.data()

def ordenar_lista(lista, ordenacao, decrescente=True):
    """
    Argumentos da Função:
        lista: lista de números a ser ordenada.
        ordenacao: lista auxiliar de números que define a prioridade da
        ordenação.
        decrescente: variável booleana para definir se a lista `ordenacao`
        deve ser ordenada em ordem crescente ou decrescente.
    Saída:
        Uma lista com o conteúdo de `lista` ordenada com base em `ordenacao`.
    Por exemplo,
        ordenar_lista([2, 4, 5, 6], [7, 2, 5, 4])
        # retorna [2, 5, 6, 4]
        ordenar_lista([1, 5, 4, 3], [3, 8, 2, 1])
        # retorna [5, 1, 4, 3]
    """
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]


def populacao_aleatoria(n):
    """
    Argumentos da Função:
        n: Número de indivíduos
    Saída:
        Uma população aleatória. População é uma lista de indivíduos,
        e cada indivíduo é uma matriz 1x6 de variaveis (alpha, r_ganho, beta, gama, r_perda, frequencia).
    """
    # Referência: np.random.uniform()
    #             list.append()
    #             for loop (for x in lista:)
    populacao = []
    for i in range(n):
        var_positivas = np.random.uniform(0, 100, (1, 2))
        # indv: alpha[0], realiza_ganho[1], beta[2], gama[3], realiza_perda[4], frequencia[5]
        indv = np.concatenate((var_positivas, np.random.uniform(var_positivas[0], 100, (1, 1)), np.random.uniform(-100, 0, (1, 2)), np.random.randint(1, 21, (1, 1))), axis=1)
        populacao.append(indv)
    return populacao


def mutacao(individuo):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
    Saída:
        Essa função não tem saída. Ela apenas modifica os pesos do indivíduo,
        de acordo com chance CHANCE_MUT para cada peso.
    """
    # Referência: for loop (for x in lista)
    #             np.random.uniform()

    # A modificação dos pesos pode ser feita de diversas formas (vide slides)

    for j in range(len(individuo[0])-1):
        if np.random.uniform(0, 1) < CHANCE_MUT:
            individuo[0][j] *= np.random.uniform(0.5, 1.5)


def crossover(individuo1, individuo2):
    """
    Argumentos da Função:
        individuoX: matriz 1x6 com as variaveis do individuos.
    Saída:
        Um novo indivíduo com variaveis que podem vir do `individuo1`
        (com chance 1-CHANCE_CO) ou do `individuo2` (com chance CHANCE_CO),
        ou seja, é um cruzamento entre os dois indivíduos. Você também pode pensar
        que essa função cria uma cópia do `individuo1`, mas com chance CHANCE_CO,
        copia os respectivos pesos do `individuo2`.
    """
    # Referência: for loop (for x in lista)
    #             np.random.uniform()
    filho = populacao_aleatoria(1)[0]
    for j in range(len(filho[0])):
        if np.random.uniform(0, 1) < CHANCE_CO:
            filho[0][j] = individuo2[0][j]
    return filho


def calcular_fitness(individuo):
    """
    Argumentos da Função:
        individuo: matriz 1x10 com as variaveis do individuo.
    Saída:
        O fitness calculado de um indivíduo. Esse cálculo é feito por meio de um back test.
        O modo mais simples é usando fitness = rentabilidade do back test.
    """

    # SET STRATEGY
    # alpha[0], realiza_ganho[1], beta[2], gama[3], realiza_perda[4], frequencia[5]
    stg = pt(individuo[0][0], individuo[0][2], individuo[0][3], individuo[0][1], individuo[0][4])

    # RUN BACKTEST
    bt = back_test(SHARES, stg, frequency=individuo[0][5])
    return bt.run_bt()


def proxima_geracao(populacao, fitness):
    """
    Argumentos da Função:
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        A próxima geração com base na população atual.
        Para criar a próxima geração, segue-se o seguinte algoritmo:
          1. Colocar os melhores indivíduos da geração atual na próxima geração.
          2. Até que a população esteja completa:
             2.1. Escolher aleatoriamente dois indivíduos da geração atual.
             2.2. Criar um novo indivíduo a partir desses dois indivíduos usando
                  crossing over.
             2.3. Mutar esse indivíduo.
             2.4. Adicionar esse indivíduo na próxima geração
    """
    # Referência: random.choices()
    #             while loop (while condition)
    #             lista[a:b]

    # Dica: lembre-se da função `ordenar_lista(lista, ordenacao)`.
    ordenados = ordenar_lista(populacao, fitness)
    proxima_ger = ordenados[:NUM_MELHORES]

    # Adicionar os melhores indivíduos da geração atual na próxima geração

    while len(proxima_ger) < NUM_INDIVIDUOS:
        # Selecionar 2 indivíduos, realizar crosover e mutação,
        # e adicionar o novo indivíduo à próxima geração
        #
        # Você pode usar a função random.choices(populacao, weights=None, k=2) para selecionar `k`
        # elementos aleatórios da população.
        #
        # Se vc passar o argumento `weights`, os indivíduos serão escolhidos com base nos pesos
        # especificados (elementos com pesos maiores são escolhidos mais frequentemente).
        # Uma ideia seria usar o fitness como peso.
        ind1, ind2 = random.choices(populacao, k=2)
        filho = crossover(ind1, ind2)
        mutacao(filho)
        proxima_ger.append(filho)

    return proxima_ger


def mostrar_melhor_individuo(populacao, fitness, ger, rent):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.populacao_aleatoria
    Saída:
        Não há saída. Simplesmente mostra o melhor indivíduo de uma população.
    """
    # VOCÊ NÃO PRECISA MEXER NESSA FUNÇÂO

    ind = populacao[max(range(len(populacao)), key=lambda i: fitness[i])]
    fit = calcular_fitness(ind)
    print('\n                |','  alpha |r_ganho |  beta  |  gama  |r_perda |  freq   ')
    print('----------------+', '--------+' * 6)
    print('Melhor individuo:', " | ".join('{:.3f}'.format(s) for s in ind[0]))
    print('Fitness: {:.4f}'.format(fit))

    # CREATE DF RESULTADO
    # col = ['alpha', 'realiza_ganho', 'beta', 'gama', 'realiza_perda', 'frequencia', 'shares', 'rentabilidade']
    col = ['alpha', 'realiza_ganho', 'beta', 'gama', 'realiza_perda', 'frequencia']
    values = dict(zip(col, list(ind[0]) + TICKET + [fit]))
    result = pd.DataFrame(values, columns=col, index=[0])

    # CREATE DF POPULACAO
    pop = pd.DataFrame(ger, columns=col)
    pop['rentabilidade'] = rent
    pop['share'] = [TICKET for x in range(len(pop))]
    # SAVE IN EXCEL
    with pd.ExcelWriter('C:\\Nícolas\\FEA.dev\\fundo_quanti\\resultados.xlsx', mode='a') as writer:
        # result.to_excel(writer, float_format="%.2f", sheet_name='Sheet1', index=False)
        pop.to_excel(writer, float_format="%.2f", sheet_name='Sheet1', index=False)
    print("Tempo Total: ",time.process_time()-ini)



###############################
# CÓDIGO QUE RODA O ALGORITMO #
###############################

# Referência: for loop (for x in lista)
#             list.append()

# OBS: Todos os prints dentro dessa função são opcionais.
#      Eles estão aqui para facilitar a visualização do algoritmo.
ini = time.process_time()
num_geracoes = 1000000

# Crie a população usando populacao_aleatoria(NUM_INDIVIDUOS)
populacao = populacao_aleatoria(NUM_INDIVIDUOS)
geracoes = []
resultados = []
geracoes += populacao

print('ger | fitness\n----+-' + '-'*9*NUM_INDIVIDUOS)

for ger in range(num_geracoes):
    # Crie uma lista `fitness` com o fitness de cada indivíduo da população
    # (usando a função calcular_fitness e um `for` loop).
    fitness = []
    for ind in populacao:
        fitness.append(calcular_fitness(ind))

    # Atualize a população usando a função próxima_geração.
    populacao = proxima_geracao(populacao, fitness)

    # Adiciona a geracoes e resultados
    geracoes += populacao
    resultados += fitness

    print('{:3} |'.format(ger),
          ' '.join('{:.5f}'.format(s) for s in sorted(fitness, reverse=True)))

    # Opcional: parar se o fitness estiver acima de algum valor (p.ex. 300)
    # if max(fitness) > 300:
    #     break

# Calcule a lista de fitness para a última geração
fitness = []
for ind in populacao:
    fitness.append(calcular_fitness(ind))

resultados += fitness
mostrar_melhor_individuo(populacao, fitness, [x[0] for x in geracoes], resultados)