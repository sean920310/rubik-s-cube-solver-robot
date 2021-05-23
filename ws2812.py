import time
from rpi_ws281x import *
import argparse


LED_COUNT      = 54      # Number of LED pixels.

LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def colorWipe(strip, color, wait_ms=40):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def cube_color_str_dis(all_face):
    for i in range(strip.numPixels()):
        color = all_face[i]
        if color == 'y':strip.setPixelColor(i, Color(255,255,0) )
        elif color == 'w':strip.setPixelColor(i, Color(255,255,255) )
        elif color == 'o':strip.setPixelColor(i, Color(255, 25, 0) )
        elif color == 'r':strip.setPixelColor(i, Color(255,0,0) )
        elif color == 'g':strip.setPixelColor(i, Color(0,255,0) )
        elif color == 'b':strip.setPixelColor(i, Color(0,0,255) )
        elif color == 'N':strip.setPixelColor(i, Color(0,0,0) )
        else:strip.setPixelColor(i, Color(0,0,0) )  
    strip.show()
        


    




# Main program logic follows:
if __name__ == '__main__':


    

    while True:
        
        colorWipe(strip, Color(255, 0, 0))  # Red wipe
        colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        colorWipe(strip, Color(0, 0, 255))  # Green wipe
        
        cube_color_str_dis('yoowybrrbwygyrbbgggyoobogbwrwrowrbgobrwwobrgywworggyyy')
        time.sleep(5)
        

        #colorWipe(strip, Color(255, 25, 0))  # Red wipe

