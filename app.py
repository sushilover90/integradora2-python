import sys
from threading import Thread
import Servo
import websocket
import netifaces as ni
import time
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
servo = Servo.Servo()

try:
    import thread
except ImportError:
    import _thread as thread

def on_message(ws, message):

    pp.pprint(message)

    _message = json.loads(message)
    
    event = _message['d']['event']
    
    if event == 'start_servo':
        print(1)
        t = Thread(target=servo.activate(),daemon=True)
        t.start()
#    try:
#
#        _message = json.loads(message)
#        
#        event = _message['d']['event']
#
#        if event == 'start_servo':
#            print(1)
#            t = Thread(target=servo.activate(),daemon=True)
#            t.start()
#
#    except: 
#        print('Error')


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run():
        ws.send('{"t":1,"d":{"topic":"servo"}}')
    Thread(target=run).start()

if __name__ == "__main__":

    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    pp.pprint(ip)
    websocket.enableTrace(True)
    ws_server_url = f'ws://{ip}:3333/adonis-ws'
    ws = websocket.WebSocketApp(ws_server_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    try:
        while True:
            ws.on_open = on_open
            ws.run_forever()
    except KeyboardInterrupt:
        sys.exit(1)
