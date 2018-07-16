#!/usr/bin/python
# -*- coding: latin-1 -*-

# ------------------------------------------------------------------------------------------------
# Auteurs : Joey Boivin et Julien Burson
# Date : 18 juillet 2018
# Cours : ELE 778 a l'Ecole de Technologie Superieure
# Nom du fichier : Learning.py
#
# **Les accents n'ont pas ete utilise intentionnellement pour des raisons de compatibilitees**
#
# Fonction du fichier :
# ------------------------------------------------------------------------------------------------

import random
import numpy as np

class NeuralNetwork:

    def __init__(self, size, func_act, taux_app):

        """
        Initialisation du systeme neurologique selon la taille desiree

        :param size: Liste du nombre d'unites par couche, incluant l'entree et la sortie
        :param func_act: La fonction d'activivation utlise pour l'apprentissage du systeme
        :param taux_app: Le taux d'appentissage du MLP

        """
        self.size = size
        self.num_layers = len(size)
        self.func_act = func_act
        self.taux_app = taux_app

        #Initialisation des poids de chaque couche
        self.init_weights()

    def init_weights(self):
        '''
        Cette fonction permet d'assigner une valeur initial entre -0.1 et 0.1 aux poids du reseau de neurones.
        Elle se sert du nombre de neurones avant et celle d'apres pour definir la quantite de poids necessaire,
        et ce, pour le nombre de couche choisi.

        :return: Le tableau contenant la valeur de tous les poids.
        '''
        self.weights = []
        next_layer_size = list(self.size)
        next_layer_size.pop(0)              #Retire le nombre d'unite de la premire couche

        for size, next_size in zip(self.size, next_layer_size):

            poids = 0.2*np.random.random((next_size, size)) - 0.1
            self.weights.append(poids)

        return self.weights

    def training(self,entree, sortie, epoque, reset_poids):

        if reset_poids:
            self.init_weights()
        for j in range(epoque):
            self.correc_poids = self.backpropagation(entree, sortie)
            self.weights = [x + y for x, y in zip(self.weights, self.correc_poids)]

    def backpropagation(self, entree, sortie):

        if self.func_act == 'sigmoid':
            def df(x): return self.dsigmoid(x)
        elif self.func_act == 'tanh':
            def df(x): return self.dtanh(x)
        elif self.func_act == 'loglog':
            def df(x): return self.dloglog(x)
        elif self.func_act == 'bipolar sigmoid':
            def df(x): return self.dbipolar_sigmoid(x)
        elif self.func_act == 'sin':
            def df(x): return self.dsin(x)

        # feedforward
        a, i = self.feedforward(entree)

        # Determination des signaux d'erreurs

        sign_err = [None]*self.num_layers      # Tableau pour les signaux d'erreurs selon le nombre de couches

        # Place à la fin du tableau la différence entre la sortie attendue et celle obtenue
        if self.func_act == 'sigmoid':
            sign_err[-1] = (sortie - a[-1]) * df(a[-1])
        else:
            sign_err[-1] = (sortie - a[-1]) * df(i[-1])

        for j in np.arange(self.num_layers - 2, 0, -1):
            # Pour chaque chaque couche, sauf celle de sortie --> np.arange(start,stop,step)
            poids_temp = self.weights[j]
            if self.func_act == 'sigmoid':
                sign_err[j] = df(a[j]) * (np.dot(sign_err[j+1].T, poids_temp)).T
            else:
                sign_err[j] = df(i[j]) * (np.dot(sign_err[j+1].T, poids_temp)).T

        # Determination des corrections

        correc_poids = [None]*(self.num_layers - 1)      # Tableau pour la correction des poids selon le nombre de couches

        for j in range(self.num_layers - 1):

            correc_poids[j]= np.dot(sign_err[j+1],a[j].T)*self.taux_app

        return correc_poids

    def feedforward(self, entry):
        #Apprentissage de l'entree vers la sortie

        input_layer = entry

        i = [None]*self.num_layers     #Tableau pour l'entree selon le nombre de couches
        a = [None]*self.num_layers     #Tableau pour la sortie selon le nombre de couches

        if self.func_act == 'sigmoid':
            def f(x): return self.sigmoid(x)
        elif self.func_act == 'tanh':
            def f(x): return self.tanh(x)
        elif self.func_act == 'loglog':
            def f(x): return self.loglog(x)
        elif self.func_act == 'bipolar sigmoid':
            def f(x): return self.bipolar_sigmoid(x)
        elif self.func_act == 'sin':
            def f(x): return self.sin(x)

        for j in range(self.num_layers -1):

            a[j] = input_layer        #a represente chaque donnees de l'unite d'entree pour chaque couche

            #Multiplication de l'entree et le poids pour obtenir le sortie, et ce, pour chaque couche
            i[j+1] = np.dot(input_layer.T, self.weights[j].T)
            i[j+1] = i[j+1].T

            #Fonction d'activation pour chaque multiplication de l'entree et du poids
            output_layer = f(i[j+1])

            #La sortie devient l'entree pour la prochaine couche
            input_layer = output_layer

        #Assigne la derniere sortie au tableau
        a[self.num_layers-1] = output_layer

        return a, i

    def test(self, input_x):
        '''
        Permet de valider si l'apprentissage est reussi
        :param input_x: La base de donnée qui est a tester
        :return: Les resultats de la couche de sortie du systeme de neuronne
        '''
        a, i = self.feedforward(input_x)
        sortie = a[-1]

        return sortie

    '''Fonction d'activation'''
    def sigmoid(self, x):
        return 1. / (1. + np.exp(-x))

    def dsigmoid(self, x):
        return x * (1. - x)

    def tanh(self, x):
        return np.tanh(x)

    def dtanh(self, x):
        return 1.0 - np.tanh(x)**2

    def loglog(self, x):
        return 1. - np.exp(-np.exp(x))

    def dloglog(self, x):
        return np.exp(x-np.exp(x))

    def bipolar_sigmoid(self, x):
        return (1 - np.exp(-x)) / (1 + np.exp(-x))

    def dbipolar_sigmoid(self, x):
        return 1 / (2*np.power((np.cosh(x/2)), 2))

    def sin(self, x):
        return np.sin(x)

    def dsin(self, x):
        return np.cos(x)
