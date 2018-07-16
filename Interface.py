import Tkinter as tk
import ttk
from Tkinter import *
from mlp_main import program

mlp = program()

def get_entry():
    nbUniteEntree = e1.get()
    nbcouchecache = e2.get()
    tauxApp = e3.get()
    epoque = e4.get()
    fonctionActivation = combo.get()
    poids = comboPoids.get()

    config, size = mlp.read_config()
    config[0] = nbUniteEntree
    config[1] = fonctionActivation
    config[2] = nbcouchecache
    config[4] = epoque
    config[5] = tauxApp
    config[6] = poids
    
    write_config(config)

    mlp.simulation()

def get_couche_cache(ents,root):

    i = len(ents)/2
    j=1
    infocouche=[]
    while i >0:
        infocouche.append(ents[j].get())
        j=j+2
        i=i-1

    with open('Configuration.txt', 'r') as f:
        line = f.readlines()
        poidscouche =""
        i=len(infocouche)
        j=0
        while i > 0:
            if not i == 1:
                poidscouche = poidscouche + infocouche[j] + ","
            else:
                poidscouche = poidscouche + infocouche[j] + "\n"

            j=j+1
            i=i-1

        line[7]=poidscouche
        f.close()

    with open('Configuration.txt', 'w') as f:
        i = 0
        j = len(line)
        while j > 0:
            f.writelines(line[i])
            i = i + 1
            j = j - 1
        f.close()

    root.destroy()

def write_config(config):
    with open('Configuration.txt', 'r') as f:
        line = f.readlines()
        line[1] = config[0] + "\n"
        line[3] = config[1] + "\n"
        line[5] = config[2] + "\n"
        line[9] = config[4] + "\n"
        line[11] = config[5] + "\n"
        if config[6] == "non":
            line[13]=("oui") + "\n"
        else:
            line[13] = ("non") + "\n"
        f.close()

    with open('Configuration.txt', 'w') as f:
        i = 0
        j=len(line)
        while j > 0:
            f.writelines(line[i])
            i = i + 1
            j = j - 1
        f.close()

def makeform(root, fields):
        entries = []
        config, size = mlp.read_config()
        i = 0
        nbcouche = int(e2.get())
        poids = config[3]

        while nbcouche > 0:
            if i == len(poids):
                var = StringVar(root, value='0')
            elif i > len(poids):
                var = StringVar(root, value='0')
            else:
                var = StringVar(root, value=poids[i])
            row = Frame(root)
            lab = Label(master=row, width=35, text=fields[i], anchor='center')
            ent = Entry(master=row, width=9, textvariable=var)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.extend((fields[i], ent))
            i=i+1
            nbcouche = nbcouche - 1
        return entries

def PoidsCoucheCache():

        nbcouche = int(e2.get())
        entry = {}
        i = 0
        while i < nbcouche:
            key = i
            value = 'Nombre d unite dans la couche cachee # '
            value += str(i + 1)
            entry[key] = value
            i += 1
        # nbCoucheCache
        fields = []
        i = 0
        while i < nbcouche:  # nbCoucheCache
            fields.append(entry[i])
            i += 1
        # cree la fenetre de parametres des couches cachees
        root = Tk()
        root.title('PARAMETRES DES COUCHES CACHEES')
        ents = makeform(root, fields)
        b1 = tk.Button(root, text='Suivant', command=lambda: get_couche_cache(ents,root))
        b1.pack(side=RIGHT, anchor='se')
        b1.bind("<Button>", lambda x: get_couche_cache(ents,root))
        b2 = tk.Button(root, text='Quitter', command=root.destroy)
        b2.pack(side=LEFT, anchor='sw')



# ------------------------------------------------------------------------------------------------
# DEBUT INTERFACE GRAPHIQUE
# ------------------------------------------------------------------------------------------------
# definition de la fenetre d'execution la simulation
windows = tk.Tk()
windows.title('MLP ELE 778')
windows.geometry("1400x750")
windows.resizable(width=False, height=False)
back = tk.Frame(master=windows)
back.pack_propagate(0)
back.pack(fill=tk.BOTH, expand=1)



# Les variables ci dessous appartiennent a l'emplacement frame
frame = Frame(windows, width=400, height=750)
frame.place(x=0, y=0)
# Bouton lancer la simulation
parametres = []
x=0
buttonSimulation = tk.Button(frame, text='Lancer la simulation', command=lambda : get_entry)
buttonSimulation.place(x=130, y=640)
# Bouton parametes des couches cachees
buttonCoucheCache = tk.Button(frame, text='Poids des couches caches', command= PoidsCoucheCache)
buttonCoucheCache.place(x=130, y=600)
# boutton quitter la simulation
buttonQuit = tk.Button(windows, text='QUITTER', command=windows.destroy)
buttonQuit.pack(side=RIGHT, anchor='sw')
# Les parametres du systeme
# Texte Nombre de ligne en entree :
var = StringVar()
label = Label(frame, textvariable=var)
var.set("Nombre de ligne en entree :")
label.place(x=10, y=200)
# text Nombre de couche cache :
var = StringVar()
label = Label(frame, textvariable=var)
var.set("Nombre de couche cache :")
label.place(x=10, y=230)
# text taux d'apprentissage :
var = StringVar()
label = Label(frame, textvariable=var)
var.set("Taux d'apprentissage:")
label.place(x=10, y=260)
# text Choix de la fonction d'activation:
var = StringVar()
label = Label(frame, textvariable=var)
var.set("Choix de la fonction d'activation:")
label.place(x=10, y=290)
# text nombre epoque apprentissage :
var = StringVar()
label = Label(frame, textvariable=var)
var.set("Nombre d'epoque d'apprentissage :")
label.place(x=10, y=320)
# text reprendre la derniere config d'apprentissage :
var = StringVar()
label = Label(frame, textvariable=var)
var.set("Voulez vous reprendre la derniere \n configuration ? ")
label.place(x=10, y=360)

# lit les information dans le fichier txt config.txt
config, size = mlp.read_config()


# initialise les variables des entry a 0
value1 = StringVar(frame, value=config[0])
value2 = StringVar(frame, value=config[2])
value3 = StringVar(frame, value=config[5])
value4 = StringVar(frame, value=config[4])

# entree Nombre de ligne en entree :
e1 = Entry(frame, width=9, textvariable=value1)
e1.place(x=260, y=200)
# entree Nombre de couche cache :
e2 = Entry(frame, width=9, textvariable=value2)
e2.place(x=260, y=230)
# entree taux d'apprentissage :
e3 = Entry(frame, width=9, textvariable=value3)
e3.place(x=260, y=260)
# menu deroulant choix de la fonction d'activation:
combo = ttk.Combobox(frame, width=9)
combo.place(x=260, y=290)
combo['values'] = ('sigmoid', 'tanh', 'loglog', 'bipolar sigmoid', 'sin')
if config[1] == 'sigmoid':
    combo.current(0)
elif config[1] == 'tanh':
    combo.current(1)
elif config[1] == 'loglog':
    combo.current(2)
elif config[1] == 'bipolar sigmoid':
    combo.current(3)
elif config[1] == 'sin':
    combo.current(4)

# entree nombre epoque apprentissage :
e4 = Entry(frame, width=9, textvariable=value4)
e4.place(x=260, y=320)

#menu deroulant afin de choisir ou non la derniere configuration
comboPoids = ttk.Combobox(frame, width=9)
comboPoids.place(x=260, y=360)
comboPoids['values'] = ('non', 'oui')
comboPoids.current(0)

# Les variables ci dessous appartiennent a l'emplacement frametext
# texte d'explication de la simulation
frametext = Frame(windows, width=1000, height=150)
frametext.place(x=400, y=0)
# text :
var = StringVar()
label = Label(frametext, textvariable=var)
var.set("Bonjour, et bienvenue dans l'unite d'apprentissage d'un MLP a retropropagation d'erreur")
label.place(x=120, y=20)
# text :
var = StringVar()
label = Label(frametext, textvariable=var)
var.set("Vous avez le choix de faire aprendre vous meme votre propre reseau de neurones")
label.place(x=120, y=40)
# text :
var = StringVar()
label = Label(frametext, textvariable=var)
var.set("Ou bien de juste tester le reseau avec un ficher de poids deja appris a l'avance")
label.place(x=120, y=60)

#lors de l'appui sur lancer la simulation cela va recuperer les
#entree de l'utilisateur et lancer la simulation
buttonSimulation.bind("<Button>", lambda x: get_entry())


windows.mainloop()
