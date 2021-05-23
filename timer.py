import time
import RPi.GPIO as GPIO

ST = 16
SH = 20
D  = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ST, GPIO.OUT)
GPIO.setup(SH, GPIO.OUT)
GPIO.setup(D , GPIO.OUT)
def GPIO_setup():
    ST = 16
    SH = 20
    D  = 21

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ST, GPIO.OUT)
    GPIO.setup(SH, GPIO.OUT)
    GPIO.setup(D , GPIO.OUT)

def send_time_595(time_in):
    dis_num = int(time_in*1000)
    num_array = [0,0,0,0,0]
    for i in range(5):
        num_array[i] = dis_num%10
        dis_num = int(dis_num/10)
    
    print(num_array)
    GPIO.output(ST, 0)
    for i in range(5):
        for j in range(8):
            GPIO.output(SH, 0)
            if(i==4 and num_array[i]==0):
                GPIO.output(D, 1)
            else:
                GPIO.output(D, seven_dis[ num_array[i] ][7-j])#seven_dis[ num_array[i] ][j]
            GPIO.output(SH, 1)
    GPIO.output(ST, 1)
    time.sleep(0.2)
    GPIO.output(SH, 0)
    GPIO.output(ST, 0)
    GPIO.output(D,  0)
    
    
    
class my_timer:
    def __init__(self):
        self.start_time = 0.0
        self.stop_time_reg = 0.0
        self.if_in_count = 0
        GPIO_setup()
    def start(self):
        self.stop_time_reg = 0.0
        self.if_in_count = 1
        send_time_595(0.0)
        self.start_time = time.time()
        
    def stop(self):
        self.stop_time_reg = round( time.time()-self.start_time , 3 )
        send_time_595(self.stop_time_reg)
    def get_pass_time(self):
        if self.if_in_count==0:
            return round( 0.0 , 3 )
        elif self.stop_time_reg>0.0:
            return round( self.stop_time_reg , 3 )
        else:
            return round( time.time()-self.start_time , 3 )

seven_dis=[
        [False,False,False,False,False,False,False,True,],
        [False,True, False,False,True, True, True, True,],
        [False,False,False,True, False,False,True, False,],
        [False,False,False,False,False,True, True, False,],
        [False,True, False,False,True, True, False,False,],
        [False,False,True, False,False,True, False,False,],
        [False,False,True, False,False,False,False,False,],
        [False,False,False,False,True, True, True, True,],
        [False,False,False,False,False,False,False,False,],
        [False,False,False,False,False,True, False,False,],
    ]


    
    












if __name__=='__main__':
    
    timer1 = my_timer()
    timer1.start()
    time.sleep(0.318)
    timer1.stop()
    '''
    while(1):
        
        #print(timer1.get_pass_time())
        send_time_595(timer1.get_pass_time())
    
    '''
    
    


