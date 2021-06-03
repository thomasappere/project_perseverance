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

jeu = Game()
jeu.fenetre.mainloop()
