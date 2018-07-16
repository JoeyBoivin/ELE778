#!/usr/bin/python
# -*- coding: latin-1 -*-

# ------------------------------------------------------------------------------------------------
# Auteurs : Joey Boivin et Julien Burson
# Date : 18 juillet 2018
# Cours : ELE 778 a l'Ecole de Technologie Superieure
# Nom du fichier : mlp_main.py
#
# **Les accents n'ont pas ete utilise intentionnellement pour des raisons de compatibilitees**
#
# Fonction du fichier : Ce fichier permet l'execution et la realisation d'un systeme d'apprentissage
#                       neuronique.
# ------------------------------------------------------------------------------------------------

import random
import numpy as np
from learning import NeuralNetwork
from AdaptFile import adaptation
import matplotlib.pyplot as plt

class program:

    def choice_in_out(self, fichier, aleatoire):
        '''
        Fonction permettant de selectionner une donnee, aleatoirement ou non, dans le fichier correspondant
        et d'en retirer les informations necessaire pour obtenir un vecteur pour les donnes d'entrees et
        un autre vecteur pour ceux de sorties.

        :param fichier: Le fichier texte contenant les donnees a analyser
        :param aleatoire: -1 : Indique que la fonction choisi une donnee au hasard
                         <=0 : Indique de choisir les donnees en ordre dans le fichier
        :return: train_x : La donnee en entree
                 train_y : La donnee attentue en sortie
        '''
        train_x = []
        word = []
        train_y = []

        with open(fichier) as f:
            line = f.readlines()

        # Elimine l'element de saut de ligne extrait par la fonction readlines()
        for i in range(len(line)):
            word_tmp = line[i].split()
            word.insert(i, word_tmp[1])

        # Choisi une donne aleatoire parmis les x donnees du fichier
        if aleatoire < 0:
            choix = random.randint(0, len(word) - 1)
        else:
            choix = aleatoire

        out_temp = word[choix].split('/')
        out_temp = out_temp[-1].split('.')
        number, letter = out_temp[0]

        if number == '1':
            train_y = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif number == '2':
            train_y = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        elif number == '3':
            train_y = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        elif number == '4':
            train_y = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        elif number == '5':
            train_y = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        elif number == '6':
            train_y = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        elif number == '7':
            train_y = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        elif number == '8':
            train_y = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        elif number == '9':
            train_y = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        elif number == 'o':
            train_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

        train_y = np.array(train_y)
        train_y = np.vstack(train_y)

        with open('temp/' + word[choix]) as f:

            line2 = f.readline()

            while line2:
                line2 = line2.splitlines()
                line2 = line2[0].split()
                train_x.append(line2)
                line2 = f.readline()

        train_x = np.array(train_x)
        train_x = train_x.flatten()         # Train_X est maintenant un tableau d'une dimension avec x*26 termes.
        train_x = np.vstack(train_x)        # Tableau vertical
        train_x = train_x.astype(np.float)  # Tableau de string converti en float

        return train_x, train_y

    def write_weigths(self, performance, epoque):
        '''
        Fonction permettant l'ecriture des poids finaux a la suite de l'execution du MLP. Ces points sont stockes dans
        un fichier «poids» et les caracteristiques du MLP sont egalement ecrit sur le fichier.

        :param performance: Variable contenant la performance des donnes de test
        :return: None
        '''
        with file('poids.txt', 'w') as f:
            f.write('# Fonction: %s\n'
                    '# Nombre unites entree: %i\n'
                    '# Nombre unites de sortie: %i\n'
                    '# Nombre epoques: %i\n'
                    '# Performance obtenue : %.2f%%\n'
                    '#\n' % (self.mlp.func_act, self.mlp.size[0], self.mlp.size[-1], epoque, performance*100.0))
            index = 1
            for i in range(len(self.mlp.size)-2):
                f.write('# Nombre unites de la couche %i: %i\n'
                        '#\n' % (i+1, self.mlp.size[i+1]))
            index2 = 1
            for j in self.mlp.weights:
                f.write('# Couche %i\n' % index2)
                np.savetxt(f, j)
                index2 = index2 + 1

    def collect_weights(self):
        '''
        Fonction qui permet de recuperer les poids de la derniere configuration dans le fichier «poids»

        :return: Les poids du dernier apprentissage effectue par le MLP
        '''

        test = np.loadtxt('poids.txt', dtype=object)

        poids_tmp = [map(float, j) for j in test]
        poids = [None] * (self.mlp.num_layers - 1)
        start = 0
        for x in range((self.mlp.num_layers - 1)):
            end = start + self.mlp.size[x+1]
            poids[x] = poids_tmp[start:end]
            start = end
            poids[x] = np.array(poids[x])

        return poids

    def train(self, epoque, iterations):
        '''
        Fonction qui permet d'entrainer le systeme selon le nombre d'epoque et d'iteration des donnes d'entrainement.
        Permet d'apprendre, mais egalement de tester le systeme a la suite de x epoque

        :param epoque: Le nombre d'epoque a effectuer
        :param iterations: Le nombre d'iterations a effectuer selon le nombre d'elements dans le fichier info_train
        :return: Un tableau des resultats(0 a 1) obtenus a la suite de x epoque
        '''

        reussi = 0.0
        result = []
        for i in range(epoque):

            for j in range(iterations):
                input_x, output_y = self.choice_in_out('info_train.txt', -1)
                self.mlp.training(input_x, output_y, 1, 0)
                Y_hat = self.mlp.test(input_x)
                y_tmp = np.argmax(Y_hat)
                y = np.argmax(output_y)
                if y_tmp == y:
                    reussi = reussi + 1
                else:
                    reussi = reussi
            result.append(reussi / iterations)
            reussi = 0.0
        return result

    def validation(self, iterations, ordre):
        '''
        Effectue une propagation de l'entree vers la sortie et en verifie l'exactitude du resultat obtenu.
        Emmagasine les resultats positifs et revoie le taux de reussite obtenu a la suite de x iterations.

        :param iterations: Le nombre d'iterations a effectuer selon le nombre d'elements dans le fichier info_vc
        :param ordre: Variable de 0 a x iterations pour preciser la ligne a analyser dans le fichier info_vc
        :return: Taux de reussite
        '''

        reussi = 0.0
        for i in range(iterations):

            input_x, output_y = self.choice_in_out('info_vc.txt', ordre)
            Y_hat = self.mlp.test(input_x)
            y_tmp = np.argmax(Y_hat)
            y = np.argmax(output_y)
            if y_tmp == y:
                reussi = reussi + 1
            else:
                reussi = reussi
            ordre = ordre + 1

        return reussi / iterations

    def test(self, iterations, ordre):
        '''
        Effectue une propagation de l'entree vers la sortie et en verifie l'exactitude du resultat obtenu.
        Emmagasine les resultats positifs et revoie le taux de reussite obtenu a la suite de x iterations.

        :param iterations: Le nombre d'iterations a effectuer selon le nombre d'elements dans le fichier info_test
        :param ordre: Variable de 0 a x iterations pour preciser la ligne a analyser dans le fichier info_test
        :return: Taux de reussite
        '''
        reussi = 0.0

        for i in range(iterations):

            input_x, output_y = self.choice_in_out('info_test.txt', ordre)
            Y_hat = self.mlp.test(input_x)
            y_tmp = np.argmax(Y_hat)
            y = np.argmax(output_y)
            if y_tmp == y:
                reussi = reussi + 1
            else:
                reussi = reussi
            ordre = ordre + 1

        return reussi / iterations

    def read_config(self):
        '''
        Lecture du fichier de configuration et permet d'en resortir l'information(voir ci-dessous) pour
        le bon fonctionnement du systeme.

        :return: config : Tableau contenant toute l'informations utile du fichier de configuration.
                 size : Tableau contenant le nombre d'unite pour chaque couche du MLP
        '''
        config = []

        with open('Configuration.txt') as f:
            lines = f.readlines()
            config.append(int(lines[1]))            # Nombre d'entree - 0
            config.append(lines[3].rstrip('\n'))    # Fonction d'activation - 1
            config.append(int(lines[5]))            # Nombre de couche cachee - 2
            nbrUnite = lines[7].split(',')        # Separation du nombre d'unite des couches cachees - 3
            nbrUnite[-1] = nbrUnite[-1].rstrip('\n')
            config.append(nbrUnite)
            config.append(int(lines[9]))            # Nombre d'epoque - 4
            config.append(float(lines[11]))         # Taux d'apprentissage - 5
            config.append(lines[13].rstrip('\n'))   # Apprentissage ou non - 6
        if config[6] == 'oui':
            config[6] = 1
        else:
            config[6] = 0

        size = []
        size.append(config[0] * 26)
        for i in config[3]:
            size.append(int(i))
        size.append(10)


        return config, size

    def graph(self, train, validation, test, epoque):
        #Creation d'un graphique illustrant les resultats obtenus

        x_train = np.arange(1, len(train)+1)
        x_valid = np.arange(epoque, len(train)+1, epoque)
        plt.plot(x_train, train * 100., '-bo', label='Entrainement')
        plt.plot(x_valid, validation * 100., '-go', label='Validation')
        plt.xticks(np.arange(min(x_train), max(x_train)+1, 1.0))
        plt.yticks(np.arange(test*100-5.0, max(train)*100+2.0, 1.0))
        plt.text(1.01, train[-1]*100, 'Performance de test: ' + str('{:.2f}'.format(test*100)) + '%')
        plt.ylabel(u'Pourcentage réussite')
        plt.xlabel(u'Époques')
        plt.title(u"Performance de l'apprentissage")
        plt.legend(loc=4)
        for a, b in zip(x_train, train*100):
            plt.text(a+0.01, b-0.4, str('{:.2f}'.format(b)))
        for a, b in zip(x_valid, validation * 100):
            plt.text(a+0.01, b-0.4, str('{:.2f}'.format(b)))
        plt.show()

    def simulation(self):
        '''
        Fonction principale qui permet d'appeler les fonctions necessaires permettant l'apprentissage.

        :return: None
        '''

        train_iterations = 1340         # Nombre d'elements du fichier d'entrainement
        valid_iterations = 120          # Nombre d'elements du fichier de validation
        test_iterations = 780           # Nombre d'elements du fichier de test

        config, size = self.read_config()
        file_adapt = adaptation()
        file_adapt.execute()            # Permet d'adapter les fichiers de donnees a partir de la classe

        epoque = config[4]              # Recuperation du nombre d'epoque a effectuer
        learn = config[6]               # 1 ou 0 , si oui, apprend a nouveau, si non, utilise la derniere configuration

        '''
        Envoie des parametres et craation du modale d'analyse du MLP.
        config[1] : Fonction d'activation lu du fichier de configuration
        config[5] : Taux d'apprentissage lu du fichier de configuration
        '''
        self.mlp = NeuralNetwork(size=size,
                            func_act=config[1],
                            taux_app=config[5])
        performance_train = []          # Tableau pour enregistrer les pourcentage de réussite de l'entrainement
        performance_valid = []          # Tableau pour enregistrer les pourcentage de réussite de la validation

        if learn:

            '''Realisation de l'entrainement et enregistrement des performances'''
            performance_train.extend((self.train(epoque, train_iterations)))

            '''Realisation de la validation et enregistrement des performances'''
            performance_valid.append((self.validation(valid_iterations, 0)))
            iteration = 0

            '''Objectif vise a 85% de reussite'''
            while performance_valid[iteration] < 0.85:
                if iteration == 0:
                    break
                performance_train.extend(self.train(epoque, train_iterations))
                performance_valid.append(self.validation(valid_iterations, 0))
                iteration += 1

            '''Realisation de la generalisation(test) et enregistrement des performances'''
            performance_test = self.test(test_iterations, 0)
        else:
            self.mlp.weights = self.collect_weights()
            performance_test = self.test(test_iterations, 0)

        self.write_weigths(performance_test, epoque)

        performance_train = np.array(performance_train)
        performance_valid = np.array(performance_valid)

        self.graph(performance_train, performance_valid, performance_test, epoque)