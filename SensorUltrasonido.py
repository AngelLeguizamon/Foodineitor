from hcsr04 import HCSR04
from time import sleep

medidor = HCSR04 (trigger_pin = 5 , echo_pin = 18)
for i in range (60):
    distancia = 100
    area = 80
    densidad = 0.1
    try:
        distancia = round(medidor.distance_cm ()*2)/2
        #print ("Distancia = ", distancia, " cm")
    except:
        print ("Error!")
    print((100-distancia)*area*densidad, "Gramos")
    
    sleep(1)