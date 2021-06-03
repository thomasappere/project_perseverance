from tkinter import *
import time

gravity = 3.8
central_thrust_max = 40
lateral_thrust_max = 5

class Game:
    def __init__(self):
        self.fenetre = Tk() #fenêtre par défaut. Tk() est un objet
        self.fenetre.title("Simulation de l'atterrissage de Perseverance sur Mars") #titre de la fenêtre
        self.fenetre.resizable(False, False) #redimensionnement de la fenêtre impossible ni en largeur, ni en hauteur
        self.canevas = Canvas(self.fenetre, width=700, height=700) #paramètres de la zone de dessin
        self.canevas.pack() #ajoute la zone de dessin à la fenêtre
        self.fond = PhotoImage(file = 'landingSite.gif')
        self.canevas.create_image(0, 0, anchor=NW, image=self.fond)
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
    def __init__(self, x, y, vx, vy, image_lander):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.delta_x = 0
        self.delta_y = 0
        self.central_thrust = 0
        self.left_thrust = 0
        self.right_thrust = 0
        self.time = time.time()
        self.widget_lander = jeu.canevas.create_image(self.x, self.y, anchor=NW, image=image_lander)

    def deplacer(self):
        if self.y >= landing_site.y1-200: #200 est la hauteur de l'image lander.gif
            if self.x < landing_site.x1 or self.x > landing_site.x2-95: #95 est la largeur de l'image lander.gif
                jeu.canevas.create_text(60,200, text='Zone d\'atterrissage ratée !', anchor=NW, font=('Helvetica', '48', 'bold'))
            jeu.enfonction = False
            return

        now = time.time()
        time_elapsed = now - self.time
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
        self.vx = self.vx + time_elapsed * (self.left_thrust - self.right_thrust)
        self.vy = self.vy + time_elapsed * (gravity - self.central_thrust)
        self.delta_x = time_elapsed * self.vx + 0.5 * (self.left_thrust - self.right_thrust) * time_elapsed**2
        self.delta_y = time_elapsed * self.vy + 0.5 * (gravity - self.central_thrust) * time_elapsed**2
        self.x = self.x + self.delta_x
        self.y = self.y + self.delta_y
        jeu.canevas.move(self.widget_lander, self.delta_x, self.delta_y)
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
            if perseverance.y < landing_site.y1-200: #200 est la hauteur de l'image lander.gif
                self.rocket = jeu.canevas.create_image(perseverance.x+self.x_rocket, perseverance.y+self.y_rocket, anchor=NW, image=self.image_rocket)

    def deplacer(self):
        jeu.canevas.delete(self.rocket)
        if self.allume == True  and perseverance.y < landing_site.y1-200: #200 est la hauteur de l'image lander.gif
            self.rocket = jeu.canevas.create_image(perseverance.x+self.x_rocket, perseverance.y+self.y_rocket, anchor=NW, image=self.image_rocket)

jeu = Game()

image_lander = PhotoImage(file = 'lander.gif')
perseverance = Lander(500, 0, 0, 100, image_lander)

landing_site = Rectangle(290, 620, 410, 625, 'red')

image_central_rocket = PhotoImage(file = 'pousseeCentrale.gif')
image_left_rocket = PhotoImage(file = 'pousseeLateraleGauche.gif')
image_right_rocket = PhotoImage(file = 'pousseeLateraleDroite.gif')
central_rocket = Retrorocket(image_central_rocket, 22, 48, '<KeyPress-Down>')
left_rocket = Retrorocket(image_left_rocket, -26, 15, '<KeyPress-Left>')
right_rocket = Retrorocket(image_right_rocket, 87, 15, '<KeyPress-Right>')
jeu.sprites.append(perseverance)
jeu.sprites.append(central_rocket)
jeu.sprites.append(left_rocket)
jeu.sprites.append(right_rocket)
jeu.boucle_principale()

#jeu.fenetre.mainloop()
