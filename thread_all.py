import threading

from servo_ctrl import*
from ws2812 import*

from cam_cap_img import*
from color_test import*
import time

from UART_to_arduino import*
from python_kociemba import*

def thread_servo_on():
    threading.Thread(target= servo_on()  ).start()
def thread_servo_off():
    threading.Thread(target= servo_off() ).start()
    
def thread_UD_on():
    threading.Thread(target= send_cmd_to_arduino('5')  ).start()   
def thread_UD_off():
    threading.Thread(target= send_cmd_to_arduino('4') ).start()
def thread_UD_up():
    threading.Thread(target= send_cmd_to_arduino('9')  ).start()   
def thread_UD_down():
    threading.Thread(target= send_cmd_to_arduino('6') ).start()
    

    