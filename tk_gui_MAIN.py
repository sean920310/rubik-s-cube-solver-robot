import numpy as np
import cv2
import threading
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from python_kociemba import*
from cam_cap_img_return_color import*
from timer import*
from ws2812 import*
from UART_to_arduino import*
from servo_ctrl import*

start_button = 6
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(start_button, GPIO.IN,pull_up_down=GPIO.PUD_UP)


sol=''

sol_type=1
color1='yyyyyyyyyrrrrrrrrrbbbbbbbbbwwwwwwwwwoooooooooggggggggg'
color2='yyyyyyyyyrrrrrrrrrbbbbbbbbbwwwwwwwwwoooooooooggggggggg'
WORKING = False
########################motor
def motor_turn_off():
    servo_off()
    send_cmd_to_arduino('7')
    send_cmd_to_arduino('-')
def motor_turn_off_URFDLB():
    send_cmd_to_arduino('7')
def cube_go_down():
    servo_off()
    time.sleep(1)
    send_cmd_to_arduino('8')
    send_cmd_to_arduino('+')
    send_cmd_to_arduino('6')
def cube_go_up():
    cube_color_str_dis('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
    send_cmd_to_arduino('8')
    send_cmd_to_arduino('+')
    send_cmd_to_arduino('9')
    servo_on()
    time.sleep(1)
    send_cmd_to_arduino('!')
def choose_sol_type(type_):
    global sol_type
    sol_type = type_
    
def scan():
    global sol,color1,color2
    read_color.config(text = '',bg='#FF0000' )
    for i in range(70):
        sol=''
        color1,color2 = webcam.getcolor()
        read_color.config(text = color1 )
        dis_color_on_btn()
        #bt.config(text = color1)123333333333333333333333333333
        if(i==40 or i==50 or i==60):
            send_cmd_to_arduino('*',0)
        try:
            get_python_kociemba_solve(color1)
            read_color.config(text = color1 ,bg='#00ff00')
            cube_color_str_dis(color1)
            break;
        except ValueError:
            try:
                get_python_kociemba_solve(color2)
                read_color.config(text = color2 ,bg='#00ff00')
                cube_color_str_dis(color2)
                break;
            except ValueError:
                time.sleep(0.01)
    
def get_solve():
    global sol,color1,color2,sol_type
    sol=''
    color_right = ''
    sol_label.config(text = 'solve')
    
    try:
        get_python_kociemba_solve(color1)
        color_right = color1
    except ValueError:
        try:
            get_python_kociemba_solve(color2)
            color_right = color2
        except ValueError:
            return False
    if sol_type==1:
        print(color_right)
        sol = get_python_kociemba_solve(color_right)
        
    if sol_type==2:
        print(color_right)
        sol = get_rob2_kociemba_solve(color_right)
    print(sol)
    sol_label.config(text = sol)
    return True

def solve_cube():
    global sol,color1,color2
    if sol=='':
        return
    timer1.start()
    send_cmd_to_arduino(sol_to_cmd(sol),1)
    timer1.stop()
def send_speed_to_arduino():
    speed = speed_scale.get()
    send_cmd_to_arduino( str(speed) )    

def auto_run():
    global WORKING
    if WORKING == False:
        WORKING = True
        window.config(bg='red')
        progressbar.config(value=1)
        cube_go_up()
        time.sleep(2)
        
        progressbar.config(value=2)
        scan()
        
        progressbar.config(value=3)
        B = get_solve()
        if(not B):
            cube_go_down()
            WORKING = False
            return 
            
        progressbar.config(value=4)
        solve_cube()
        
        
        progressbar.config(value=5)
        cube_go_down()
        #window.after(2000, scan )
        #window.after(2100, solve_cube )
        window.config(bg='lightblue')
        WORKING = False
    
def time_dis_on_label():
    #dis_num = round(timer1.get_pass_time() , 3 )
    time_dis.config(text ='{:.3f}'.format(round(timer1.get_pass_time() , 3 )))
    window.after(10,time_dis_on_label)
def dis_color_on_btn():
    global sol,color1,color2
    for i in range(54):
        col = color1[i]
        if(col=='y'):
            color_btn_array[i].config(bg='yellow',activebackground='yellow')
        if(col=='r'):
            color_btn_array[i].config(bg='red',activebackground='red')
        if(col=='b'):
            color_btn_array[i].config(bg='blue',activebackground='blue')
        if(col=='w'):
            color_btn_array[i].config(bg='white',activebackground='white')
        if(col=='o'):
            color_btn_array[i].config(bg='orange',activebackground='orange')
        if(col=='g'):
            color_btn_array[i].config(bg='green',activebackground='green')
        
        if(col=='E'):
            color_btn_array[i].config(bg='purple',activebackground='yellow')
        if(col=='N'):
            color_btn_array[i].config(bg='black',activebackground='yellow')
def change_color_from_btn(num):
    global sol,color1,color2
    arr1=[]
    arr2=[]
    for i in range(  len(color1) ):
        arr1.append( color1[i] ) 
    for i in range(  len(color2) ):
        arr2.append( color2[i] ) 
    print(len(color1))
    if num not in [4,13,22,31,40,49]:
        if color1[num]=='y':
            arr1[num]='r'
            arr2[num]='r'
        if color1[num]=='r':
            arr1[num]='b'
            arr2[num]='b'
        if color1[num]=='b':
            arr1[num]='w'
            arr2[num]='w'
        if color1[num]=='w':
            arr1[num]='o'
            arr2[num]='o'
        if color1[num]=='o':
            arr1[num]='g'
            arr2[num]='g'
        if color1[num]=='g':
            arr1[num]='y'
            arr2[num]='y'
        
        if color1[num]=='N':
            arr1[num]='y'
            arr2[num]='y'
        if color1[num]=='E':
            arr1[num]='y'
            arr2[num]='y'
            
    color1=''
    color2=''
    color1=''.join(arr1)
    color2=''.join(arr2)
    dis_color_on_btn()
    cube_color_str_dis(color1)
    
def check_start_button():
    if not GPIO.input(start_button):
        threading.Thread(target=auto_run).start()
    window.after(100,check_start_button)

    
######################################################################

def full_screen_sw():
    window.attributes("-fullscreen",not window.attributes("-fullscreen"))
    #bt.config(text = 'fuck')
def dis_winwow_size():
    H = window.winfo_height()
    W = window.winfo_width()
    winwow_size.config(text = 'win H:{}  W:{}'.format(H,W) )
    x = window.winfo_pointerx()
    y = window.winfo_pointery()
    mouse_pos.config(text = 'mouse X:{} Y:{}'.format(x,y) )
    window.after(100, dis_winwow_size) 
def show_frame():
    frame =webcam.getframe()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    display1.imgtk = imgtk #Shows frame for display 1
    display1.configure(image=imgtk)
    color_show,_=webcam.getcolor()
    now_color.config(text = color_show )
    #dis_color_on_btn()###########################
    window.after(10, show_frame)
##########################solve step######################
#def auto_run_all():



#start tkinter ////////////////////////////////////////////////////
webcam = WebCamCapture()

webcam.start()
timer1 = my_timer()


#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.geometry('1024x576')
window.config(background="#FFFFFF")
window.attributes("-fullscreen", True)

pixelVirtual = tk.PhotoImage(width=1, height=1)
#Graphics window
imageFrame = tk.Frame(window)
imageFrame.place(x=0, y=0)

    
    

display1 = tk.Label(imageFrame)
display1.grid(row=0, column=0)  #Display 1


#Slider window (slider controls stage position)
#sliderFrame = tk.Frame(window, width=500, height=100)
#sliderFrame.grid(row = 4, column=4, padx=10, pady=2)

now_color = tk.Label(window , text='' , bg='green')
now_color.place(x=0,y=215)
read_color = tk.Label(window , text='scan' , bg='green')
read_color.place(x=0,y=435)
sol_label = tk.Label(window , text='solve' , bg='green')
sol_label.place(x=0,y=460)

'''
fontStyle = tkFont.Font(size=7)
winwow_size = tk.Label(window , text='' , bg='orange',font=fontStyle)
winwow_size.place(x=815,y=0)
mouse_pos = tk.Label(window , text='' , bg='orange',font=fontStyle)
mouse_pos.place(x=815,y=17)
'''

#bt.config(text='(0,5)')
fontStyle = tkFont.Font(size=18)
tk.Label(window , text='速度' , bg='lightblue',font=fontStyle).place(x=975,y=35)

speed_scale=tk.Scale(window ,length=140,width=40 ,from_=4,to=0, orient="vertical",)
speed_scale.config( command = lambda self:threading.Thread(target=send_speed_to_arduino).start() )
speed_scale.place(x=975,y=70)
speed_scale.set(3)


fontStyle = tkFont.Font(size=12)
tk.Button(window , text='口' , bg='yellow', command = full_screen_sw,font=fontStyle ).place(x=990, y=0)


fontStyle = tkFont.Font(size=100)
time_dis = tk.Label(window , text='' , bg='lightyellow')
time_dis.config(image=pixelVirtual,compound="c",font=fontStyle,height = 150,width = 450)
time_dis.place(x=0,y=280)


fontStyle = tkFont.Font(size=30)
start_btn = tk.Button(window , text='開始\n自動' , bg='#39FF14', command = lambda:threading.Thread(target=auto_run).start() )
start_btn.config(image=pixelVirtual,compound="c",font=fontStyle,height = 150,width = 150)
start_btn.place(x=1024-175,y=576-160)

fontStyle = tkFont.Font(size=20)
motor_off = tk.Button(window , text='關閉馬達' , bg='red', command = lambda:threading.Thread(target=motor_turn_off).start() )
motor_off.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 100)
motor_off.place(x=815,y=215)

fontStyle = tkFont.Font(size=14)
motor_off = tk.Button(window , text='關閉URFDLB' , bg='red', command = lambda:threading.Thread(target=motor_turn_off_URFDLB).start() )
motor_off.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 100)
motor_off.place(x=815,y=270)

fontStyle = tkFont.Font(size=12)
cube_up = tk.Button(window , text='魔方\n就位' , bg='#39FF14', command = lambda:threading.Thread(target=cube_go_up).start() )
cube_up.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 40)
cube_up.place(x=130,y=490)

fontStyle = tkFont.Font(size=12)
scan_btn = tk.Button(window , text='顏色\n偵測' , bg='#39FF14', command = lambda:threading.Thread(target=scan).start() )
scan_btn.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 40)
scan_btn.place(x=290,y=490)

fontStyle = tkFont.Font(size=12)
get_solve_btn = tk.Button(window , text='算出\n解法' , bg='#39FF14', command = lambda:threading.Thread(target=get_solve).start() )
get_solve_btn.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 40)
get_solve_btn.place(x=450,y=490)

fontStyle = tkFont.Font(size=12)
solve_cube_btn = tk.Button(window , text='解出\n魔方' , bg='#39FF14', command = lambda:threading.Thread(target=solve_cube).start() )
solve_cube_btn.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 40)
solve_cube_btn.place(x=610,y=490)

fontStyle = tkFont.Font(size=12)
cube_up = tk.Button(window , text='魔方\n取出' , bg='#39FF14', command = lambda:threading.Thread(target=cube_go_down).start() )
cube_up.config(image=pixelVirtual,compound="c",font=fontStyle,height = 40,width = 40)
cube_up.place(x=770,y=490)

s = ttk.Style()
s.theme_use('clam')
s.configure("TProgressbar",troughcolor ='gray', foreground='yellow', background='#00FF00')
progressbar=ttk.Progressbar(window,style="TProgressbar",orient="horizontal",length=800,mode="determinate",phase=1)
progressbar.config(maximum=5 )
progressbar.config(value=0)
progressbar.place(x=10,y=550)

fontStyle = tkFont.Font(size=15)
sol_choose_lable = tk.Label(window , text='選擇解法' , bg='lightblue',font=fontStyle)
sol_choose_lable.place(x=815,y=0)

fontStyle = tkFont.Font(size=10)
kociemba_sol_btn = tk.Button(window , text='kociemba' , bg='lightgreen',font=fontStyle)
kociemba_sol_btn.config(command = lambda:choose_sol_type(1))
kociemba_sol_btn.place(x=815,y=30)

fontStyle = tkFont.Font(size=10)
rob2_sol_btn = tk.Button(window , text='rob-twophase' , bg='lightgreen',font=fontStyle)
rob2_sol_btn.config(command = lambda:choose_sol_type(2))
rob2_sol_btn.place(x=815,y=60)

####################################display rubik cube pick 
rubik = tk.Frame(window,bg='black')
rubik.place(x=470,y=245)


color_btn_array = []
for i in range(54):
    color_btn_array.append([])
for i in range(54):
    color_btn_array[i]=tk.Button(rubik ,activebackground='#39FF14', bg='#39FF14',relief=tk.FLAT)
    color_btn_array[i].config(image=pixelVirtual,compound="c",height = 18,width = 18)
    


color_btn_array[0].config(command = lambda:change_color_from_btn(0))
color_btn_array[1].config(command = lambda:change_color_from_btn(1))
color_btn_array[2].config(command = lambda:change_color_from_btn(2))
color_btn_array[3].config(command = lambda:change_color_from_btn(3))
color_btn_array[4].config(command = lambda:change_color_from_btn(4))
color_btn_array[5].config(command = lambda:change_color_from_btn(5))
color_btn_array[6].config(command = lambda:change_color_from_btn(6))
color_btn_array[7].config(command = lambda:change_color_from_btn(7))
color_btn_array[8].config(command = lambda:change_color_from_btn(8))

color_btn_array[9].config(command = lambda:change_color_from_btn(9))
color_btn_array[10].config(command = lambda:change_color_from_btn(10))
color_btn_array[11].config(command = lambda:change_color_from_btn(11))
color_btn_array[12].config(command = lambda:change_color_from_btn(12))
color_btn_array[13].config(command = lambda:change_color_from_btn(13))
color_btn_array[14].config(command = lambda:change_color_from_btn(14))
color_btn_array[15].config(command = lambda:change_color_from_btn(15))
color_btn_array[16].config(command = lambda:change_color_from_btn(16))
color_btn_array[17].config(command = lambda:change_color_from_btn(17))

color_btn_array[18].config(command = lambda:change_color_from_btn(18))
color_btn_array[19].config(command = lambda:change_color_from_btn(19))
color_btn_array[20].config(command = lambda:change_color_from_btn(20))
color_btn_array[21].config(command = lambda:change_color_from_btn(21))
color_btn_array[22].config(command = lambda:change_color_from_btn(22))
color_btn_array[23].config(command = lambda:change_color_from_btn(23))
color_btn_array[24].config(command = lambda:change_color_from_btn(24))
color_btn_array[25].config(command = lambda:change_color_from_btn(25))
color_btn_array[26].config(command = lambda:change_color_from_btn(26))

color_btn_array[27].config(command = lambda:change_color_from_btn(27))
color_btn_array[28].config(command = lambda:change_color_from_btn(28))
color_btn_array[29].config(command = lambda:change_color_from_btn(29))
color_btn_array[30].config(command = lambda:change_color_from_btn(30))
color_btn_array[31].config(command = lambda:change_color_from_btn(31))
color_btn_array[32].config(command = lambda:change_color_from_btn(32))
color_btn_array[33].config(command = lambda:change_color_from_btn(33))
color_btn_array[34].config(command = lambda:change_color_from_btn(34))
color_btn_array[35].config(command = lambda:change_color_from_btn(35))

color_btn_array[36].config(command = lambda:change_color_from_btn(36))
color_btn_array[37].config(command = lambda:change_color_from_btn(37))
color_btn_array[38].config(command = lambda:change_color_from_btn(38))
color_btn_array[39].config(command = lambda:change_color_from_btn(39))
color_btn_array[40].config(command = lambda:change_color_from_btn(40))
color_btn_array[41].config(command = lambda:change_color_from_btn(41))
color_btn_array[42].config(command = lambda:change_color_from_btn(42))
color_btn_array[43].config(command = lambda:change_color_from_btn(43))
color_btn_array[44].config(command = lambda:change_color_from_btn(44))

color_btn_array[45].config(command = lambda:change_color_from_btn(45))
color_btn_array[46].config(command = lambda:change_color_from_btn(46))
color_btn_array[47].config(command = lambda:change_color_from_btn(47))
color_btn_array[48].config(command = lambda:change_color_from_btn(48))
color_btn_array[49].config(command = lambda:change_color_from_btn(49))
color_btn_array[50].config(command = lambda:change_color_from_btn(50))
color_btn_array[51].config(command = lambda:change_color_from_btn(51))
color_btn_array[52].config(command = lambda:change_color_from_btn(52))
color_btn_array[53].config(command = lambda:change_color_from_btn(53))



color_btn_array[0 ].grid(padx=1,pady=1,row=0,column=3)
color_btn_array[1 ].grid(padx=1,pady=1,row=0,column=4)
color_btn_array[2 ].grid(padx=1,pady=1,row=0,column=5)
color_btn_array[3 ].grid(padx=1,pady=1,row=1,column=3)
color_btn_array[4 ].grid(padx=1,pady=1,row=1,column=4)
color_btn_array[5 ].grid(padx=1,pady=1,row=1,column=5)
color_btn_array[6 ].grid(padx=1,pady=1,row=2,column=3)
color_btn_array[7 ].grid(padx=1,pady=1,row=2,column=4)
color_btn_array[8 ].grid(padx=1,pady=1,row=2,column=5)

color_btn_array[9 ].grid(padx=1,pady=1,row=3,column=6)
color_btn_array[10].grid(padx=1,pady=1,row=3,column=7)
color_btn_array[11].grid(padx=1,pady=1,row=3,column=8)
color_btn_array[12].grid(padx=1,pady=1,row=4,column=6)
color_btn_array[13].grid(padx=1,pady=1,row=4,column=7)
color_btn_array[14].grid(padx=1,pady=1,row=4,column=8)
color_btn_array[15].grid(padx=1,pady=1,row=5,column=6)
color_btn_array[16].grid(padx=1,pady=1,row=5,column=7)
color_btn_array[17].grid(padx=1,pady=1,row=5,column=8)

color_btn_array[18].grid(padx=1,pady=1,row=3,column=3)
color_btn_array[19].grid(padx=1,pady=1,row=3,column=4)
color_btn_array[20].grid(padx=1,pady=1,row=3,column=5)
color_btn_array[21].grid(padx=1,pady=1,row=4,column=3)
color_btn_array[22].grid(padx=1,pady=1,row=4,column=4)
color_btn_array[23].grid(padx=1,pady=1,row=4,column=5)
color_btn_array[24].grid(padx=1,pady=1,row=5,column=3)
color_btn_array[25].grid(padx=1,pady=1,row=5,column=4)
color_btn_array[26].grid(padx=1,pady=1,row=5,column=5)

color_btn_array[27].grid(padx=1,pady=1,row=6,column=3)
color_btn_array[28].grid(padx=1,pady=1,row=6,column=4)
color_btn_array[29].grid(padx=1,pady=1,row=6,column=5)
color_btn_array[30].grid(padx=1,pady=1,row=7,column=3)
color_btn_array[31].grid(padx=1,pady=1,row=7,column=4)
color_btn_array[32].grid(padx=1,pady=1,row=7,column=5)
color_btn_array[33].grid(padx=1,pady=1,row=8,column=3)
color_btn_array[34].grid(padx=1,pady=1,row=8,column=4)
color_btn_array[35].grid(padx=1,pady=1,row=8,column=5)

color_btn_array[36].grid(padx=1,pady=1,row=3,column=0)
color_btn_array[37].grid(padx=1,pady=1,row=3,column=1)
color_btn_array[38].grid(padx=1,pady=1,row=3,column=2)
color_btn_array[39].grid(padx=1,pady=1,row=4,column=0)
color_btn_array[40].grid(padx=1,pady=1,row=4,column=1)
color_btn_array[41].grid(padx=1,pady=1,row=4,column=2)
color_btn_array[42].grid(padx=1,pady=1,row=5,column=0)
color_btn_array[43].grid(padx=1,pady=1,row=5,column=1)
color_btn_array[44].grid(padx=1,pady=1,row=5,column=2)

color_btn_array[45].grid(padx=1,pady=1,row=3,column=9)
color_btn_array[46].grid(padx=1,pady=1,row=3,column=10)
color_btn_array[47].grid(padx=1,pady=1,row=3,column=11)
color_btn_array[48].grid(padx=1,pady=1,row=4,column=9)
color_btn_array[49].grid(padx=1,pady=1,row=4,column=10)
color_btn_array[50].grid(padx=1,pady=1,row=4,column=11)
color_btn_array[51].grid(padx=1,pady=1,row=5,column=9)
color_btn_array[52].grid(padx=1,pady=1,row=5,column=10)
color_btn_array[53].grid(padx=1,pady=1,row=5,column=11)




'''
def dis_W_H():
    #b1.config(text = b1.text+="1")
    text = window['text']
    print(text)
window.after(10, dis_W_H())
bt.cget("text")
#w.winfo_height()
#w.winfo_width()
'''
show_frame() #Display
check_start_button()
#dis_winwow_size()
time_dis_on_label()
dis_color_on_btn()



window.mainloop()  #Starts GUI

#b1.config(text='fuck')
