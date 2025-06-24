import machine
import time
from machine import Pin
from  time import sleep
import urequests as rq

lockstat=True
unlockstat=True
TELEGRAM_BOT_TOKEN = '7503505246:AAH9HlQTREtYtXAvRp1b9zIjLXfCIpjc0N8'
TELEGRAM_BOT_ID = '6119294750'
TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_BOT_TOKEN)

def do_connect():
    SSID='Private'
    PASSWORD='12345678'
    import network
    wlan = network.WLAN(network.STA_IF)                        
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        #wlan.connect('LAPTOP-0FTK45F2 3896', '8V6387f')
        wlan.connect(SSID,PASSWORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ipconfig('addr4'))

def send_telegram_message(message):
    payload = {'chat_id':TELEGRAM_BOT_ID,'text':message}
    try:
        rq.post(TELEGRAM_API_URL,json=payload)
        return True
    except Exception as e:
        print("Error Sending Message",e)
        return False



d=Pin(0,Pin.IN)
#current_time = time.gmtime()
#current_date = time.localtime()

buzzer=Pin(15,Pin.OUT)
#buzzer.value(0)

def dataupload(d):
    api = 'https://door-lock-system-3c238-default-rtdb.firebaseio.com/.json'
    print('sending data...')
    re = rq.post(api,json=d).text
    print(re)

do_connect()
while True:
   
        doorstat=d.value()
        print('Status:',doorstat)
        
        dt = time.localtime()
        y = dt[0]
        mo = dt[1]
        day = dt[2]
        h = dt[3]
        m = dt[4]
        s = dt[5]
        
        date = f'{day}/{mo}/{y}'
        ti = f'{h}:{m}:{s}'
        
        
        
        dic = {
                'status': doorstat,
                'time':ti,
                'date':date
            }
        
        sleep(0.2)
        if (doorstat == 0):
            buzzer.value(0)
            print("Door is locked")
            
            if lockstat == True:
                dataupload(dic)
                lockstat = False 
                unlockstat = True
            
        elif (doorstat == 1):
      
            print(f"Alert!Door is unlocked at: {date} {ti}")
            
            buzzer.value(1)
            buzzer.on()
            sleep(0.3)
            buzzer.value(0)
            sleep(0.3)
            lockstat = True
            
            if unlockstat == True:
                dataupload(dic)
                send_telegram_message("Door is unlocked")
                unlockstat = False
            
                
        else:
            print("no sensor applied")