# NAME:
#    	atterrissage_perseverance.py
#
# PURPOSE:
#    	Simulation de l'atterrissage du rover Perseverance dans le cratère Jezero, planète Mars
#       Le but est de faire atterrir le rover sur la barre rouge avec une vitesse verticale vy <= 20.
#
# CALLING SEQUENCE:
#       Dans le Terminal, taper : python3 atterrissage_perseverance.py
#       Ou exécuter ce programme dans un IDE Python.
#       Pour relancer le jeu, exécuter de nouveau le programme.
#       Lorsqu'on ferme la fenêtre, une erreur apparaît, c'est normal.
#
# INPUTS:
#
# OUTPUTS:
#    	Affichage d'une fenêtre graphique tkinter
#
# COMMENTS:
#    	La touche Bas active la rétrofusée centrale, un nouvel appui sur la touche Bas la désactive.
#       La touche Gauche active la rétrofusée gauche, un nouvel appui sur la touche Gauche la désactive.
#       La touche Droite active la rétrofusée droite, un nouvel appui sur la touche Droite la désactive.
#
# PROCEDURES AND FUNCTIONS USED:
#
#
# MODIFICATION HISTORY:
#       Programme inspiré de https://briggs.net.nz/python-for-kids/puzzles/project1-lander.py.txt
#       Créé entre juin et août 2020 par Thomas Appéré thomas.appere@ac-rennes.fr

from tkinter import *
import time
import matplotlib.pyplot as plt
import numpy as np

#Canevas (canvas en anglais) = zone de l'écran où on peut dessiner

pesanteur_martienne = 3.8 #Intensité de la pesanteur sur Mars (en m/s^-2)
poussee_retrofusee_centrale_max = -40 #poussée maximale due à la rétrofusée centrale (selon y)
poussee_retrofusee_laterale_max = 5 #poussée maximale due aux rétrofusées latérales (selon x)
v_max = 10 #Vitesse maximale à l'atterrissage (en m/s)

class Game:
    #Classe qui forme le contrôleur principal du programme
    def __init__(self):
        self.fenetre = Tk() #fenêtre par défaut (Tk est lui-même un objet)
        self.fenetre.title("Simulation de l'atterrissage de Perseverance sur Mars") #titre de la fenêtre
        self.fenetre.resizable(False, False) #redimensionnement de la fenêtre impossible ni en largeur, ni en hauteur
        self.canevas = Canvas(self.fenetre, width=700, height=700) #paramètres de la zone de dessin
        self.canevas.pack() #pour que la zone de dessin se redimensionne aux dimensions données à la ligne précédente
        self.fenetre.update()
        self.hauteur_canevas = self.canevas.winfo_height()
        self.largeur_canevas = self.canevas.winfo_width()
        self.fond = PhotoImage(file = 'landing_site.gif')
        self.canevas.create_image(0, 0, anchor=NW, image=self.fond)
        self.titre = self.canevas.create_text(140,5, text='18 février 2021, cratère Jezero, planète Mars', anchor=NW, font=('Helvetica', '20', 'bold'))
        self.succes_texte = self.canevas.create_text(10,75, text='Pour gagner, il faut atterrir dans la \nzone d\'atterrissage avec vy <= '+str(v_max)+' m/s', anchor=NW)
        self.lutins = []
        self.enfonction = True

    def boucle_principale(self):
        while 1: #boucle qui ne s'arrête que lorsqu'on ferme la fenêtre de jeu
            if self.enfonction == True:
                for lutin in self.lutins:
                    lutin.deplacer()
            self.fenetre.update()
            time.sleep(0.05)

class Lander:
    #Classe pour créer le lander = rover muni de son module d'atterrissage
    def __init__(self, jeu):
        self.canevas = jeu.canevas
        self.image_lander = PhotoImage(file = 'lander_v2.gif')
        self.lander = jeu.canevas.create_image(500, -50, anchor=NW, image=self.image_lander)
        self.time = time.time() #instant de démarrage du jeu
        self.vx = 0 #vitesse initiale du lander selon x
        self.vy = 100 #vitesse initiale du lander selon y
        self.x = self.canevas.coords(self.lander)[0] #position initiale du lander selon x
        self.y = self.canevas.coords(self.lander)[1]#position initiale du lander selon y
        self.delta_x = 0 #deplacement du lander selon x (en px/pas de temps)
        self.delta_y = 0 #deplacement du lander selon y (en px/pas de temps)
        self.poussee_retrofusee_centrale = 0 #poussée instantanée de la rétrofusée centrale
        self.poussee_retrofusee_gauche= 0 #poussée instantanée de la rétrofusée gauche
        self.poussee_retrofusee_droite = 0 #poussée instantanée de la rétrofusée droite
        self.bas = False #rétrofusées touche haut
        self.gauche = False #rétrofusées touche gauche
        self.droite = False #rétrofusées touche droite
        jeu.canevas.bind_all('<KeyPress-Down>', self.allumage_retrofusee_centrale) #bind_all : pour lier l'événement à tous les widgets de l'application
        jeu.canevas.bind_all('<KeyPress-Left>', self.allumage_retrofusee_gauche)
        jeu.canevas.bind_all('<KeyPress-Right>', self.allumage_retrofusee_droite)
        self.poussee_centrale_texte = self.canevas.create_text(10,35, text='poussee retrofusee centrale = '+str(int(self.poussee_retrofusee_centrale))+' N', anchor=NW)
        self.poussee_laterale_texte = self.canevas.create_text(10,50, text='poussee retrofusees laterales = '+str(int(self.poussee_retrofusee_gauche) - int(self.poussee_retrofusee_droite))+' N', anchor=NW)
        self.vitesse_texte = self.canevas.create_text(10,105, text='vy = '+str(int(self.vy))+' m/s', anchor=NW)

    def allumage_retrofusee_centrale(self, evt): #l'objet evt (événement) doit être inclus en paramètre sinon Python déclenche une erreur
        if self.bas == True:
            self.bas = False
            self.poussee_retrofusee_centrale = 0
        else:
            self.bas = True

    def allumage_retrofusee_gauche(self, evt): #l'objet evt (événement) doit être inclus en paramètre sinon Python déclenche une erreur
        if self.gauche == True:
            self.gauche = False
            self.poussee_retrofusee_gauche = 0
        else:
            self.gauche = True

    def allumage_retrofusee_droite(self, evt): #l'objet evt (événement) doit être inclus en paramètre sinon Python déclenche une erreur
        if self.droite == True:
            self.droite = False
            self.poussee_retrofusee_droite = 0
        else:
            self.droite = True

    def deplacer(self):
        if self.y >= 420: #l'image lander_v2.gif fait 200 px de hauteur et le sol est à y=620
            if self.vy > v_max:
                jeu.message_final = self.canevas.create_text(270,200, text='BOOM !', anchor=NW, font=('Helvetica', '48', 'bold'))
                jeu.enfonction = False
            elif self.x < 290 or self.x > 410-90:
                jeu.message_final = self.canevas.create_text(60,200, text='Zone d\'atterrissage ratée !', anchor=NW, font=('Helvetica', '48', 'bold'))
                jeu.enfonction = False
            else:
                jeu.message_final = self.canevas.create_text(120,200, text='We\'re safe on Mars !', anchor=NW, font=('Helvetica', '48', 'bold'))
                jeu.enfonction = False
            return

        maintenant = time.time() #instant à l'appel de la fonction deplacer()
        temps_ecoule = maintenant - self.time
        if self.bas == True:
            self.poussee_retrofusee_centrale = poussee_retrofusee_centrale_max
        if self.gauche == True:
            self.poussee_retrofusee_gauche = poussee_retrofusee_laterale_max
        if self.droite == True:
            self.poussee_retrofusee_droite = poussee_retrofusee_laterale_max
        self.vx = self.vx + temps_ecoule * (self.poussee_retrofusee_gauche - self.poussee_retrofusee_droite)
        self.vy = self.vy + temps_ecoule * (pesanteur_martienne + self.poussee_retrofusee_centrale)
        self.delta_x = temps_ecoule * self.vx + 0.5 * (self.poussee_retrofusee_gauche - self.poussee_retrofusee_droite) * temps_ecoule**2
        self.delta_y = temps_ecoule * self.vy + 0.5 * (pesanteur_martienne + self.poussee_retrofusee_centrale) * temps_ecoule**2
        self.canevas.move(self.lander, self.delta_x, self.delta_y) #ATTENTION : ici, self.delta_y est compris comme un delta y qui s'ajoute à la position précédente
        self.x = self.canevas.coords(self.lander)[0] #position du lander selon x
        self.y = self.canevas.coords(self.lander)[1] #position du lander selon y
        self.canevas.itemconfig(self.vitesse_texte, text='vy = '+str(int(self.vy))+' m/s')
        self.canevas.itemconfig(self.poussee_centrale_texte, text ='poussee retrofusee centrale = '+str(int(self.poussee_retrofusee_centrale))+' N')
        self.canevas.itemconfig(self.poussee_laterale_texte, text ='poussee retrofusees laterales = '+str(int(self.poussee_retrofusee_gauche)-int(self.poussee_retrofusee_droite))+' N')
        self.time = time.time()

class Central_rocket:
    #Classe pour créer l'image de la rétrofusée centrale
    def __init__(self, jeu, perseverance):
        self.canevas = jeu.canevas
        self.image_central_rocket_on = PhotoImage(file = 'poussee_centrale.gif')
        self.central_rocket_on = jeu.canevas.create_image(perseverance.x+22, perseverance.y+48, anchor=NW, image=self.image_central_rocket_on, state='hidden')
    def deplacer(self):
        self.central_rocket_on = jeu.canevas.delete(self.central_rocket_on)
        if perseverance.y >= 420:
            return
        if perseverance.bas == True:
            self.central_rocket_on = jeu.canevas.create_image(perseverance.x+22, perseverance.y+48, anchor=NW, image=self.image_central_rocket_on)

class Left_rocket:
    #Classe pour créer l'image de la rétrofusée gauche
    def __init__(self, jeu, perseverance):
        self.canevas = jeu.canevas
        self.image_left_rocket_on = PhotoImage(file = 'pousseelateraleGauche.gif')
        self.left_rocket_on = jeu.canevas.create_image(perseverance.x-26, perseverance.y+15, anchor=NW, image=self.image_left_rocket_on, state='hidden')
    def deplacer(self):
        self.left_rocket_on = jeu.canevas.delete(self.left_rocket_on)
        if perseverance.y >= 420:
            return
        if perseverance.gauche == True:
            self.left_rocket_on = jeu.canevas.create_image(perseverance.x-26, perseverance.y+15, anchor=NW, image=self.image_left_rocket_on)

class Right_rocket:
    #Classe pour créer l'image de la rétrofusée droite
    def __init__(self, jeu, perseverance):
        self.canevas = jeu.canevas
        self.image_right_rocket_on = PhotoImage(file = 'pousseelateraleDroite.gif')
        self.right_rocket_on = jeu.canevas.create_image(perseverance.x+87, perseverance.y+15, anchor=NW, image=self.image_right_rocket_on, state='hidden')
    def deplacer(self):
        self.right_rocket_on = jeu.canevas.delete(self.right_rocket_on)
        if perseverance.y >= 420:
            return
        if perseverance.droite == True:
            self.right_rocket_on = jeu.canevas.create_image(perseverance.x+87, perseverance.y+15, anchor=NW, image=self.image_right_rocket_on)

class Debris:
    #Classe pour créer les débris
    def __init__(self, jeu, perseverance):
        self.canevas = jeu.canevas
        self.image_debris = PhotoImage(file = 'debris2.gif')
    def deplacer(self):
        if perseverance.y >=420 and perseverance.vy > v_max:
            perseverance.image_lander = jeu.canevas.delete(perseverance.image_lander)
            self.debris = jeu.canevas.create_image(perseverance.x-90, perseverance.y+160, anchor=NW, image=self.image_debris)

class Sol:
    #Classe pour créer le sol
    def __init__(self, jeu):
        self.canevas = jeu.canevas
        self.sol = self.canevas.create_rectangle(290, 620, 410, 625, fill='red') #canevas.create_rectangle(x0,y0,x1,y1,option...)

jeu = Game()
perseverance = Lander(jeu)
surface_martienne = Sol(jeu)
retrofusee_centrale = Central_rocket(jeu, perseverance)
retrofusee_gauche = Left_rocket(jeu, perseverance)
retrofusee_droite = Right_rocket(jeu, perseverance)
debris = Debris(jeu, perseverance)
jeu.lutins.append(perseverance)
jeu.lutins.append(retrofusee_centrale)
jeu.lutins.append(retrofusee_gauche)
jeu.lutins.append(retrofusee_droite)
jeu.lutins.append(debris)
jeu.boucle_principale()