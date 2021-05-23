import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

servo_min = 250  # Min pulse length out of 4096
servo_max = 575  # Max pulse length out of 4096

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

def servo_off():
    pwm.set_pwm(0, 0, servo_min)
    pwm.set_pwm(1, 0, servo_min)
    pwm.set_pwm(2, 0, servo_min)
    pwm.set_pwm(3, 0, servo_min)
    
def servo_on():
    pwm.set_pwm(1, 0, servo_max)
    pwm.set_pwm(0, 0, servo_max)
    pwm.set_pwm(2, 0, servo_max)
    pwm.set_pwm(3, 0, servo_max)

if __name__ == '__main__':
    while True:
        cmd = input("Enter to continue...")
        if cmd == '0':
            servo_off()
        if cmd == '1':
            servo_on()
        
            
    
        
    

