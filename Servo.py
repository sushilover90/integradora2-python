import RPi.GPIO as GPIO
from time import sleep


class Servo:

    active = False
    pwm = None

    def __init__(self):
        return

    def __set_angle(self, angle):
        duty = angle / (10 + 2)
        GPIO.output(7, True)
        self.pwm.ChangeDutyCycle(duty)
        print('before sleep')
        sleep(1)
        GPIO.output(7, False)
        self.pwm.ChangeDutyCycle(0)

    def __deactive(self):
        self.pwm.stop()
        self.pwm = None
        GPIO.cleanup()
        self.active = False
        print('deactivated')

    def activate(self):
        if not self.active:
            self.active = True

    def start(self):
        print('starting')
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(7, GPIO.OUT)
        self.pwm = GPIO.PWM(7, 100)
        self.pwm.start(0)
        self.__set_angle(65)
        self.__set_angle(155)
        self.__set_angle(65)
        print('done')
        self.__deactive()

    def is_active(self) -> bool:
        return self.active
