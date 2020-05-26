from m5stack import *
from m5ui import *
from uiflow import *
import network ##only import if you want to connect to M5Stack AP
import wifiCfg  
import socket  

rgb.set_screen([0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#rgb.setColor(1, 0xff0000)

state = 0 #state variable for the leds

#function for displaying the html   
def web_page():
  #if state = 0:
   # rgb.setColor(2, 0x33cc00)
    #else:
        #led_state="On"
        
 html = """<html><head> <title>M5Stack Web Server</title></head><body><h1>Atom Web Server</h1><strong>""" + str(state) + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p><p><a href="/?led=off"><button class="button button2">OFF</button></a></p>"""  
 return html

response = None  
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32')
ap.config(authmode=3, password='123456789')   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind(('192.168.4.1', 80))  
s.listen(5)  

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    
    if led_on == 6:
        state = 1
        #label5.setText('LED ON')
        #rgb.setColor(2, 0x33cc00)
        rgb.setColorAll(0xffffff)
    if led_off == 6:
        state = 0
        #label5.setText('LED OFF')
        #rgb.setColor(2, 0xff0000)
        rgb.setColorAll(0x000000)
    
    
    #print ('Content = %s' % request)
    #lcd.print('Content = %s' % request,0,50,0xffffff)
    if ap.isconnected() == True:
        rgb.setColor(1, 0x33cc00)
    else:
        rgb.setColor(1, 0xff0000)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
