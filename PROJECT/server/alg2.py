#!/usr/bin/env python3
import pandas as pd
import numpy as np
import random 
import os
import time
import matplotlib.pyplot as plt
import algorithms
import asyncio
from decimal import *
from deap import base
from deap import creator
from deap import tools
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.metrics import precision_score, recall_score, auc, accuracy_score, roc_auc_score,f1_score,log_loss, classification_report, roc_curve
import warnings
warnings.filterwarnings("ignore");

np.set_printoptions(precision=8)
def maxFitness(individual, X_train, X_test, y_train, y_test):
    rf = RandomForestClassifier(n_estimators=individual[0], criterion=individual[1], 
                                max_depth=individual[2], min_samples_split=individual[3])
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    m = metrics.f1_score(y_test, y_pred)
    return (m),

def mutate(individual, muta):
    if muta == '1':
        i = random.randint(1,4)
        if i == 1:
            individual[0]=random.randint(10, 300)
        elif i == 2:
            individual[1] = random.choice(['gini', 'entropy'])
        elif i == 3:
            individual[2] = random.choice([random.randint(2, 10), None])
        else:
            individual[3] = random.choice([2, 3, 4])

    elif muta == '2':
        individual[0]=random.randint(10, 300)
        individual[1] = random.choice(['gini', 'entropy'])
        individual[2] = random.choice([random.randint(2, 10), None])
        individual[3] = random.choice([2, 3, 4])

    elif muta == '3':
        individual[0] = int(individual[0]*random.gauss(1, 0.5))
    return (individual),

async def GA(socket, sel='1', mate='1', PC=0.9, muta='1', PM=0.1, sizeP=5, sizeI=10):

    df = pd.read_csv("C:/Users/Kseniya/Desktop/diplom/PROJECT/server/dataNEW.csv") 
    df = df.drop('Unnamed: 0', axis=1)
    X = df.drop('BAD', axis=1)
    y = df['BAD']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, shuffle=True, random_state=123)

    # константы генетического алгоритма
    POPULATION_SIZE = sizeI   # количество индивидуумов в популяции
    P_CROSSOVER = PC      # вероятность скрещивания
    P_MUTATION = PM    # вероятность мутации индивидуума
    MAX_GENERATIONS = sizeP  # максимальное количество поколений

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("n_estimators", random.randint, 10, 300)
    toolbox.register("criterion", random.choice, ['gini', 'entropy'])
    toolbox.register("max_depth", random.choice, [random.randint(2, 10), None])
    toolbox.register("min_samples_split", random.choice, [2, 3, 4])
    
    toolbox.register("individualCreator", tools.initCycle, creator.Individual, 
                     (toolbox.n_estimators, toolbox.criterion, toolbox.max_depth, toolbox.min_samples_split), 1)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    population = toolbox.populationCreator(n=POPULATION_SIZE)

    toolbox.register("evaluate", maxFitness, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)

    if sel == '1':
        toolbox.register("select", tools.selTournament, tournsize=3)
    elif sel == '2':
        toolbox.register("select", tools.selRoulette)
    elif sel == '3':
        toolbox.register("select", tools.selRandom)
    elif sel == '4':
        toolbox.register("select", tools.selBest)
    

    if mate == '1':
        toolbox.register("mate", tools.cxOnePoint)
    elif mate == '2':
        toolbox.register("mate", tools.cxTwoPoint)
    elif mate == '3':
        toolbox.register("mate", tools.cxUniform, indpb=0.5)

    toolbox.register("mutate", mutate, muta=muta)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)
    stats.register("std", np.std)

    
    HALL_OF_FAME_SIZE = 10
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    population, logbook = await algorithms.eaSimple(population, toolbox,
                                                    cxpb=P_CROSSOVER,
                                                    mutpb=P_MUTATION,
                                                    ngen=MAX_GENERATIONS,
                                                    stats=stats,
                                                    halloffame=hof,
                                                    verbose=True,
                                                    socket=socket,
                                                    code=2,
                                                    model=RandomForestClassifier,
                                                    X_train=X_train, 
                                                    X_test=X_test, 
                                                    y_train=y_train, 
                                                    y_test=y_test)
    await asyncio.sleep(2)