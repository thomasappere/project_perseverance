# project_perseverance
Update on 3/1/2021:
pesanteur_martienne = 3.8 #Intensité de la pesanteur sur Mars (en m/s^-2)
poussee_retrofusee_centrale_max = -40 #poussée maximale due à la rétrofusée centrale (selon y)
poussee_retrofusee_laterale_max = 5 #poussée maximale due aux rétrofusées latérales (selon x)
v_max = 10 #Vitesse maximale à l'atterrissage (en m/s)

Simulation of Perseverance landing in Jezero crater with Python.
The skycrane is controlled with keypad:
- Press kp-down to turn on the central retrorocket and press it again to turn it off.
- Press kp-left to turn on the left retrorocket and press it again to turn it off.
- Press kp-right to turn on the right retrorocket and press it again to turn it off.
The goal is to land on the red rectangle with a vertical speed vy <= v_max.
