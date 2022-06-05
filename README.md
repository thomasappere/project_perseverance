# project_perseverance
Update on 3/1/2021:
- gravity = 3.8 #gravity on Mars (in m/s^-2)
- central_thrust_max = 73000. #maximal thrust due to central retrorocket (selon y)
- lateral_thrust_max = 9000 #maximal thrust due to lateral retrorockets (selon x)
- vmax = 15 #maximal vertical speed for a successful landing (en m/s)

and other changes in the code such as a larger tolerance for landing.

Simulation of Perseverance landing in Jezero crater with Python.
The skycrane is controlled with keypad:
- Press kp-down to turn on the central retrorocket and press it again to turn it off.
- Press kp-left to turn on the left retrorocket and press it again to turn it off.
- Press kp-right to turn on the right retrorocket and press it again to turn it off.
The goal is to land on the red rectangle with a vertical speed vy <= v_max.
