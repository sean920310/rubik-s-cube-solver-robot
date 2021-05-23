import serial
import timer

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout = 5)
ser.flush()

def send_cmd_to_arduino(cmd,if_return=1):
    ser.flushInput()
    ser.write( (cmd + '\n\r').encode() )
    if if_return==1:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline(5000).decode()
                return line

if __name__ == '__main__':
    
    cmd = '80vFrcSkrbKoKrEbEqGqGzFk'
    timer1 = timer.my_timer()
    timer1.start()
    print( send_cmd_to_arduino(cmd) )
    print( timer1.get_pass_time() )
    
    
   

        
            
        
