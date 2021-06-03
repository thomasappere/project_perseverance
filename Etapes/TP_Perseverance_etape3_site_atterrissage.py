from tkinter import *


class Game:
    def __init__(self):
        self.fenetre = Tk() #fenêtre par défaut. Tk() est un objet
        self.fenetre.title("Simulation de l'atterrissage de Perseverance sur Mars") #titre de la fenêtre
        self.fenetre.resizable(False, False) #redimensionnement de la fenêtre impossible ni en largeur, ni en hauteur
        self.canevas = Canvas(self.fenetre, width=700, height=700) #paramètres de la zone de dessin
        self.canevas.pack() #ajoute la zone de dessin à la fenêtre
        self.fond = PhotoImage(file = 'landingSite.gif')
        self.canevas.create_image(0, 0, anchor=NW, image=self.fond)

class Lander:
    def __init__(self, x, y, vx, vy, image_lander):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        jeu.canevas.create_image(self.x, self.y, anchor=NW, image=image_lander)

class Rectangle:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        jeu.canevas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = color)

jeu = Game()

image_lander = PhotoImage(file = 'lander.gif')
perseverance = Lander(500, 0, 0, 100, image_lander)

landing_site = Rectangle(290, 620, 410, 625, 'red')
jeu.fenetre.mainloop()
