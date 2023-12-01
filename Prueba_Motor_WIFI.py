from machine import Pin
from time import sleep
import network
import socket

def Conectar_Red(Net_name:str,Password:str):
    global sta_if
    sta_if = network.WLAN(network.STA_IF) # Instanciamos el objeto -sta_if- para controlar la interfaz STA
    if not sta_if.isconnected():
        while not sta_if.isconnected():
            sta_if.active(True)# Activamos la interfaz STA del ESP32
            sta_if.connect(Net_name,Password)# Iniciamos la conexion con los datos de nuestro AP
            print("Connecting to network ", Net_name +"...")
    else:
        #print('CONFIGURACION DE RED(IP/MASCARA/GATEWAY/DNS:', sta_if.ifconfig())
        lista = sta_if.ifconfig()
        print("Succesfuly connected :D")
        print("Your IP number is",lista[0])

def Rotar_Motor_Steper(leds,mover = 1):
    for i in range(1024):leds[(1024+mover*i)%4].value(True);leds[(1024+mover*(i-1))%4].value(False);sleep(0.01)
    print("El motor terminó su curso")

def Pagina_Web():
    html="""<!DOCTYPE html>
    <html>
        <head><title>Control de un motor</title></head>
        <body>
            <a href=/?motor=ON><button style='width=330px;height=100px'>Adelante</button></a>
            <a href=/?motor=OFF><button style='width=330px;height=100px'>Atras</button></a>
            <input type="range" name="red" min="0" max="255" step="15">
            <a href=/?servomotores><button style='width=330px;height=100px'>Enviar</button></a>
        </body>
    </html> 
    """
    return html

# Iniciamos la conexion con los datos de nuestro AP
#Conectar_Red("santi_25", "lila1301")
#Conectar_Red("Camp Nou","JuanCamilo")
#Conectar_Red("CLARO-4B58","Cl4r0@664B58")
Conectar_Red("Redmi Note 8","porfavor")

#Se crean los pines de salida
"""
led1 = Pin(5,Pin.OUT,value=False)
led2 = Pin(18,Pin.OUT,value=False)
led3 = Pin(19,Pin.OUT,value=False)
led4 = Pin(21,Pin.OUT,value=False)
"""
leds = [Pin(x,Pin.OUT,value=False) for x in (13,12,14,27)]

delay = 0.5

#Se crea el socket para el server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',80))
s.listen(5)

while True:
    cl,addr = s.accept()
    print("Cliente conectado desde ",addr)
    request = cl.recv(1024)
    request = str(request)
    print("Contenido = ",request)
    
    MotorON = request.find("/?motor=ON")
    MotorOFF = request.find("/?motor=OFF")
    ServoMotor = request.find("/?servomotor")
    
    if MotorON == 6:
        print("Motor Encendido")
        Rotar_Motor_Steper(leds,1)
    elif MotorOFF == 6:
        print("Motor en Reversa")
        Rotar_Motor_Steper(leds,-1)
    elif ServoMotor == 6:
        print("jajaja")
    respuesta = Pagina_Web()
    cl.send("HTTP/1.1 200 Ok\n")
    cl.send("Content-Type: text/html\n")
    cl.send("Connection: close\n\n")
    cl.sendall(respuesta)
    cl.close()

#Rotar_Motor_Steper(leds,True)