# NAME:
#    	atterrissage_perseverance.py
#
# PURPOSE:
#    	Simulation de l'atterrissage du rover Perseverance dans le cratère Jezero, planète Mars
#       Le but est de faire atterrir le rover sur la barre rouge avec une vitesse verticale vy <= 15.
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
#       Pour rendre le jeu plus dynamique, on peut utiliser la combinaison de valeurs : gravity = 38, central_thrust_max = 200, vmax = 50.
#
# PROCEDURES AND FUNCTIONS USED:
#
#
# MODIFICATION HISTORY:
#       Programme inspiré de https://briggs.net.nz/python-for-kids/puzzles/project1-lander.py.txt
#       Créé entre juin et août 2020 par Thomas Appéré thomas.appere@ac-rennes.fr

from tkinter import *
from pygame import mixer
import time

mixer.init() #pour le son des retrofusees
mixer.music.load("retrofusee.mp3")

gravity = 3.8
central_thrust_max = 73000.
lateral_thrust_max = 9000.
vmax = 15.

class Game:
    def __init__(self):
        self.fenetre = Tk() #fenêtre par défaut. Tk() est un objet
        self.fenetre.title("Simulation de l'atterrissage de Perseverance sur Mars") #titre de la fenêtre
        self.fenetre.resizable(False, False) #redimensionnement de la fenêtre impossible ni en largeur, ni en hauteur
        self.windowWidth = 700
        self.windowHeight = 700
        self.canevas = Canvas(self.fenetre, width=self.windowWidth, height=self.windowHeight) #paramètres de la zone de dessin
        self.canevas.pack() #ajoute la zone de dessin à la fenêtre
        self.fond = PhotoImage(file = 'landingSite.gif')
        self.canevas.create_image(0, 0, anchor=NW, image=self.fond)
        self.canevas.create_text(self.windowWidth/2,15, text='18 février 2021, cratère Jezero, planète Mars', font=('Helvetica', '20', 'bold'))
        self.canevas.create_text(10,75, text='Pour gagner, il faut atterrir dans la \nzone d\'atterrissage avec vy <= '+str(vmax)+' m/s', anchor=NW)
        self.sprites = []
        self.enfonction = True

    def boucle_principale(self):
        while 1:
            if self.enfonction == True:
                for sprite in self.sprites:
                    sprite.deplacer()
            self.fenetre.update()
            time.sleep(0.05)

class Lander:
    def __init__(self, x, y, vx, vy, image_lander, mass_lander):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass_lander = mass_lander
        self.delta_x = 0
        self.delta_y = 0
        self.central_thrust = 0
        self.left_thrust = 0
        self.right_thrust = 0
        self.time = time.time()
        self.widget_lander = jeu.canevas.create_image(self.x, self.y, anchor=NW, image=image_lander)
        self.vtext = jeu.canevas.create_text(10,105, text='vy = '+str(int(self.vy))+' m/s', anchor=NW, font=('Helvetica', '15', 'bold'))
        self.central_thrust_text = jeu.canevas.create_text(10,35, text='poussee retrofusee centrale = '+str(abs(int(self.central_thrust)))+' N', anchor=NW)
        self.lateral_thrust_text = jeu.canevas.create_text(10,50, text='poussee retrofusees laterales = '+str(int(self.left_thrust) - int(self.right_thrust))+' N', anchor=NW)

    def deplacer(self):
        if self.y >= landing_site.y1-200: #200 est la hauteur de l'image lander.gif
            if self.vy >= vmax:
                jeu.canevas.create_text(jeu.windowWidth/2, 200, text='BOOM !', font=('Helvetica', '48', 'bold'))
                mixer.music.stop()
                mixer.music.load("explosion.mp3")
                mixer.music.play()
            elif self.x < landing_site.x1 or self.x > landing_site.x2-83:
                jeu.canevas.create_text(jeu.windowWidth/2, 200, text='Zone d\'atterrissage ratée !', font=('Helvetica', '30', 'bold'))
                mixer.music.stop()
                mixer.music.load("out_of_landing_site.mp3")
                mixer.music.play()
            else:
                jeu.canevas.create_text(jeu.windowWidth/2, 200, text='We\'re safe on Mars !', font=('Helvetica', '30', 'bold'))
                mixer.music.stop()
                mixer.music.load("touchdown.mp3")
                mixer.music.play()
            jeu.enfonction = False
            return

        now = time.time()
        delta_t = now - self.time
        if central_rocket.allume == True:
            self.central_thrust = central_thrust_max
        if left_rocket.allume == True:
            self.left_thrust = lateral_thrust_max
        if right_rocket.allume == True:
            self.right_thrust = lateral_thrust_max
        if central_rocket.allume == False:
            self.central_thrust = 0
        if left_rocket.allume == False:
            self.left_thrust = 0
        if right_rocket.allume == False:
            self.right_thrust = 0

        if not central_rocket.allume and not left_rocket.allume and not right_rocket.allume: #toutes retrofusees eteintes
            mixer.music.stop()
        else:
            mixer.music.play() #au moins une retrofusee allumee

        delta_vx = delta_t * (self.left_thrust - self.right_thrust)/self.mass_lander
        delta_vy = delta_t * (gravity - self.central_thrust/self.mass_lander)
        self.vx = self.vx + delta_vx
        self.vy = self.vy + delta_vy
        self.delta_x = delta_t * self.vx
        self.delta_y = delta_t * self.vy
        self.x = self.x + self.delta_x
        self.y = self.y + self.delta_y
        jeu.canevas.move(self.widget_lander, self.delta_x, self.delta_y)
        if self.vy > vmax:
            color='red'
        else:
            color='green'
        jeu.canevas.itemconfig(self.vtext, text='vy = '+str(int(self.vy))+' m/s', fill=color)
        jeu.canevas.itemconfig(self.central_thrust_text, text ='poussee retrofusee centrale = '+str(abs(int(self.central_thrust)))+' N')
        jeu.canevas.itemconfig(self.lateral_thrust_text, text ='poussee retrofusees laterales = '+str(int(self.left_thrust)-int(self.right_thrust))+' N')
        self.time = time.time()

class Rectangle:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        jeu.canevas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = color)

class Retrorocket:
    #Classe pour créer et déplacer l'image d'une rétrofusée
    def __init__(self, image_rocket, x_rocket, y_rocket, key):
        self.x_rocket = x_rocket
        self.y_rocket = y_rocket
        self.image_rocket = image_rocket
        self.rocket=jeu.canevas.create_image(perseverance.x+self.x_rocket, perseverance.y+self.y_rocket, anchor=NW, image=self.image_rocket, state='hidden')
        self.allume = False
        jeu.canevas.bind_all(key, self.allumage) #bind_all : pour lier l'événement à tous les widgets de l'application

    def allumage(self, evt):
        if self.allume == True:
            self.allume = False
            jeu.canevas.delete(self.rocket)
        else:
            self.allume = True
            if perseverance.y < landing_site.y1-200:
                self.rocket = jeu.canevas.create_image(perseverance.x+self.x_rocket, perseverance.y+self.y_rocket, anchor=NW, image=self.image_rocket)

    def deplacer(self):
        jeu.canevas.delete(self.rocket)
        if self.allume == True  and perseverance.y < landing_site.y1-200: #200 est la hauteur de l'image lander.gif
            self.rocket = jeu.canevas.create_image(perseverance.x+self.x_rocket, perseverance.y+self.y_rocket, anchor=NW, image=self.image_rocket)

class Debris:
    def __init__(self, image_debris):
        self.image_debris = image_debris

    def deplacer(self):
        if perseverance.y >= landing_site.y1-200 and perseverance.vy >= vmax: #200 est la hauteur de l'image lander.gif
            jeu.canevas.delete(perseverance.widget_lander)
            jeu.canevas.create_image(perseverance.x-90, perseverance.y+160, anchor=NW, image=self.image_debris)

jeu = Game()

image_lander = PhotoImage(file = 'lander.gif')
perseverance = Lander(500, 0, 0, 100, image_lander, 1825.)

landing_site = Rectangle(290, 620, 410, 625, 'red')

image_central_rocket = PhotoImage(file = 'pousseeCentrale.gif')
image_left_rocket = PhotoImage(file = 'pousseeLateraleGauche.gif')
image_right_rocket = PhotoImage(file = 'pousseeLateraleDroite.gif')
central_rocket = Retrorocket(image_central_rocket, 22, 48, '<KeyPress-Down>')
left_rocket = Retrorocket(image_left_rocket, -26, 15, '<KeyPress-Left>')
right_rocket = Retrorocket(image_right_rocket, 87, 15, '<KeyPress-Right>')

image_debris = PhotoImage(file = 'debris.gif')
debris = Debris(image_debris)

jeu.sprites.append(perseverance)
jeu.sprites.append(central_rocket)
jeu.sprites.append(left_rocket)
jeu.sprites.append(right_rocket)
jeu.sprites.append(debris)

jeu.boucle_principale()

#jeu.fenetre.mainloop()