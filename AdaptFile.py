#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from random import randrange

############################################
#	Permet d'adapter un fichier pour   #
#	  le nombre d'entrée désiré        #
############################################

#############
# Variables #
#############

testFile = 'info_test.txt'
trainFile = 'info_train.txt'
validationFile = 'info_vc.txt'

nubArray = []
lineArray = []

nbrEntree = int(input("Entrée le nombre d'entrée désiré: "))

with open(validationFile) as f:
    line = f.readline()
    while line:
        words = line.split()
        ecart = 0
        if int(words[0]) > nbrEntree:
            ecart = int(words[0])-nbrEntree
            print 'plus grand'
            with open(words[1]) as f2:
                line2 = f2.readline()
                x = 0
                while line2:
                    lineArray.insert(x,line2)
                    numbers = line2.split()
                    nubArray.insert(x,float(numbers[12]))
                    line2 = f2.readline()
                    x = x+1
                while ecart > 0:
                    minpos = nubArray.index(min(nubArray))
                    del lineArray[minpos]
                    del nubArray[minpos]
                    ecart = ecart-1
                f3 = open('temp/'+ words[1],'w')
                for i, elem in enumerate(lineArray):
                    f3.write(lineArray[i])
                f3.close()
                del nubArray[:]
                del lineArray[:]
        elif int(words[0]) < nbrEntree:
            print 'plus petit'
            a = []
            b = []
            average = []
            ecart = nbrEntree - int(words[0])
            with open(words[1]) as f2:
                line2 = f2.readline()
                x = 0
                while line2:
                    lineArray.insert(x, line2)
                    nubArray.insert(x, line2.split())
                    line2 = f2.readline()
                    x = x + 1
                while ecart > 0:
                    index_a = randrange(len(lineArray)-1)
                    index_b = index_a + 1
                    a = list(nubArray[index_a])
                    b = list(nubArray[index_b])
                    y = 0
                    while y < 26:
                        average.insert(y, str((float(a[y])+float(b[y]))/2))
                        y = y+1
                    average.append('\r\n')
                    ecart = ecart-1
                    lineArray.insert(index_b,' '.join(list(average)))
                    nubArray.insert(index_b, list(average))
                    del average[:]
                    del a[:]
                    del b[:]
                f3 = open('temp/' + words[1], 'w')
                for i, elem in enumerate(lineArray):
                    f3.write(lineArray[i])
                f3.close()
                del lineArray[:]
        else:
            print 'egal'
            with open(words[1]) as f2:
                with open('temp/' + words[1], 'w') as f3:
                    for line in f2:
                        f3.write(line)

        line = f.readline()