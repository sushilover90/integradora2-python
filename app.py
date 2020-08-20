import json
import pprint
import sys
import threading

import netifaces as ni
import websocket

import Servo
import Ultrasonic

pp = pprint.PrettyPrinter(indent=4)
servo = Servo.Servo()
ultra = Ultrasonic.Ultrasonic()

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    pp.pprint(message)

    _message = json.loads(message)

    event = _message['d']['event']

    if event == 'start_servo':
        # print(1)
        activate_servo()


#    try:##        _message = json.loads(message)#        #        event = _message['d']['event']##        if event == 'start_servo':#            print(1)#            t = Thread(target=servo.activate(),daemon=True)#            t.start()##    except: #        print('Error')

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run():
        ws.send('{"t":1,"d":{"topic":"iot"}}')

    threading.Thread(target=run).start()
    threading.Thread(target=send_ultra_info , daemon=True).start()


def send_ultra_info():
    while True:
        try:
            if not servo.is_active():
                ultra.start()
                distance = ultra.get_distance()
                ws.send('{"t":7,"d":{"topic":"iot","event":"measure","data":{"distance":' + str(distance) + '}}}')
        except RuntimeError:
            pass


def activate_servo():
    ws.send('{"t":7,"d":{"topic":"iot","event":"message","data":{"servo_active":true}}}')
    servo.activate()
    servo.start()
    ws.send('{"t":7,"d":{"topic":"iot","event":"message","data":{"servo_active":false}}}')


if __name__ == "__main__":

    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    pp.pprint(ip)
    websocket.enableTrace(True)
    ip = '165.227.23.126'
    ws_server_url = f'ws://{ip}:8888/adonis-ws'
    ws = websocket.WebSocketApp(ws_server_url, on_message=on_message, on_error=on_error, on_close=on_close)

    try:
        while True:
            try:
                ws.on_open = on_open
                ws.run_forever()
            except KeyboardInterrupt:
                sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
