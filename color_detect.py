import cv2
import numpy as np
from ws2812 import*

y = (0,255,255)
r = (0,0,255)
b = (255,0,0)
w = (255,255,255)
o = (0,136,255)
g = (0,255,0)

black = (0,0,0)       #color error
purple = (120,0,120)  #cover corner is error



color_pos = [
    [593,12],    [615,28],  [642,42], [566,28],  [617,53],  [541,40],  [564,53],  [591,67],  #U cov0 , 0
    [606,93], [631,78],  [656,65], [604,124], [653,94],  [603,152], [627,135], [656,123],     #R cov7 , 15
    [527,63], [549,78],  [577,92], [528,92],  [576,123], [523,124],     [553,134], [576,150], #F cov5 , 21
    [230,134],[202,147], [178,165],    [204,123], [154,147], [178,109], [151,123], [127,135], #D cov2 , 26
    [193,24], [216,41],  [244,53],    [193,51],  [241,84],  [193,82],  [219,99],  [244,112], #L cov2 , 34
    [112,51],    [141,41],  [165,24], [116,84],  [164,51],  [112,112], [136,96],  [162,81]   #B cov0 , 40
    ]                                   #cov piece is 0,15,21,26,34,40
cover_pos = [0,15,21,26,34,40]

    
d_white = [0,0,90]     #白  0,0,160
u_white = [180,100,255]      #180,42,255
d_red1 = [0,43,46]
u_red1 = [5,255,255]
d_red2 = [156,43,46]
u_red2 = [180,255,255]  #紅
d_orange = [6,43,46]
u_orange = [24,255,255] #橘
d_yellow = [25,43,46]
u_yellow = [45,255,255] #黃
d_green = [53,35,46]
u_green = [93,255,255]  #綠
d_blue = [94,43,46]
u_blue = [134,255,255]  #藍


def color_classification(hsv_color):
    
    if hsv_color[0] >= d_yellow[0] and hsv_color[0] <= u_yellow[0]:
        if hsv_color[1] >= d_yellow[1] and hsv_color[1] <= u_yellow[1]:
            if hsv_color[2] >= d_yellow[2] and hsv_color[2] <= u_yellow[2]:
                return "y"
    
    
    
    
    if (hsv_color[0] >= d_red1[0] and hsv_color[0] <= u_red1[0]) or (hsv_color[0] >= d_red2[0] and hsv_color[0] <= u_red2[0]):
        if (hsv_color[1] >= d_red1[1] and hsv_color[1] <= u_red1[1]) or (hsv_color[1] >= d_red2[1] and hsv_color[1] <= u_red2[1]):
            if (hsv_color[2] >= d_red1[2] and hsv_color[2] <= u_red1[2]) or (hsv_color[2] >= d_red2[2] and hsv_color[2] <= u_red2[2]):
                return "r"
    
    if hsv_color[0] >= d_orange[0] and hsv_color[0] <= u_orange[0]:
        if hsv_color[1] >= d_orange[1] and hsv_color[1] <= u_orange[1]:
            if hsv_color[2] >= d_orange[2] and hsv_color[2] <= u_orange[2]:
                return "o"
    
    
    
    if hsv_color[0] >= d_green[0] and hsv_color[0] <= u_green[0]:
        if hsv_color[1] >= d_green[1] and hsv_color[1] <= u_green[1]:
            if hsv_color[2] >= d_green[2] and hsv_color[2] <= u_green[2]:
                return "g"
    
    if hsv_color[0] >= d_blue[0] and hsv_color[0] <= u_blue[0]:
        if hsv_color[1] >= d_blue[1] and hsv_color[1] <= u_blue[1]:
            if hsv_color[2] >= d_blue[2] and hsv_color[2] <= u_blue[2]:
                return "b"
        
    if hsv_color[0] >= d_white[0] and hsv_color[0] <= u_white[0]:
        if hsv_color[1] >= d_white[1] and hsv_color[1] <= u_white[1]:
            if hsv_color[2] >= d_white[2] and hsv_color[2] <= u_white[2]:
                return "w"
    
    return "N"

def str_to_color(STR):
    if STR == 'y':   return y
    if STR == 'r'   :   return r
    if STR == 'b'  :   return b
    if STR == 'w' :   return w
    if STR == 'o':   return o
    if STR == 'g' :   return g
    if STR == 'E' :   return purple
    return black


def know_cover_corner(color1 , color2):
    all_possibility = [
        ['y','o','b'],['b','y','o'],['o','b','y'],
        ['y','b','r'],['r','y','b'],['b','r','y'],
        ['y','r','g'],['g','y','r'],['r','g','y'],
        ['y','g','o'],['o','y','g'],['g','o','y'],
        ['w','r','b'],['b','w','r'],['r','b','w'],
        ['w','b','o'],['o','w','b'],['b','o','w'],
        ['w','o','g'],['g','w','o'],['o','g','w'],
        ['w','g','r'],['r','w','g'],['g','r','w']
    ]
    for i in range( len(all_possibility) ):
        if color1 == all_possibility[i][0] and color2 == all_possibility[i][1]:
            return all_possibility[i][2]
    
    return 'E'
        





def circle_color(img_in):
    img=img_in
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    all_color =[]

    #color = color_classification(hsv[y,x])

    
    for i in range(len( color_pos )):
        x,y  = color_pos[i]
        
        if i not in cover_pos:
            cv2.circle(img,(x,y),6, black ,-1)
            
            color_str = color_classification(hsv[y,x])
            cv2.circle(img,(x,y),4,  str_to_color( color_str ) ,-1)
            #if x==0 and y==0:
                
            all_color.append( color_str )
        else:
            cv2.circle(img,(x,y),10, purple ,-1)
            all_color.append( 'E' )
   
    
    
    all_color[0] = know_cover_corner(all_color[42] , all_color[32])
    all_color[15] = know_cover_corner(all_color[31] , all_color[45])
    all_color[21] = know_cover_corner(all_color[39] , all_color[24])
    
    all_color[26] = know_cover_corner(all_color[13] , all_color[23])
    all_color[34] = know_cover_corner(all_color[16] , all_color[5])
    all_color[40] = know_cover_corner(all_color[2] , all_color[10])

    for i in cover_pos:
        (x,y) = color_pos[i]
        cv2.circle(img,(x,y),6,  str_to_color( all_color[i]) ,-1)
        
    

    all_color1 = all_color.copy()
    
    
    
    
    all_color2 = all_color1.copy()
    
  
    for i in range( len(all_color2) ):
        if all_color2[i]=='b':
            all_color2[i]='r'
        elif all_color2[i]=='r':
            all_color2[i]='g'
        elif all_color2[i]=='g':
            all_color2[i]='o'
        elif all_color2[i]=='o':
            all_color2[i]='b'

    all_color1.insert(4+8*0 +0,'y')
    all_color1.insert(4+8*1 +1,'r')
    all_color1.insert(4+8*2 +2,'b')
    all_color1.insert(4+8*3 +3,'w')
    all_color1.insert(4+8*4 +4,'o')
    all_color1.insert(4+8*5 +5,'g')
    
    all_color2.insert(4+8*0 +0,'y')
    all_color2.insert(4+8*1 +1,'r')
    all_color2.insert(4+8*2 +2,'b')
    all_color2.insert(4+8*3 +3,'w')
    all_color2.insert(4+8*4 +4,'o')
    all_color2.insert(4+8*5 +5,'g')
    
    all_color_str1 = ''.join(all_color1)
    all_color_str2 = ''.join(all_color2)

    #print(all_color_str1)
    #print(all_color_str2)


 
    return img , all_color_str1 , all_color_str2    #, all_face_color






if __name__=='__main__':
    #print( know_cover_corner('g' , 'o') )
    #know_cover_corner(3 , 3)
    #img=cv2.imread('/home/pi/windows_shared/frame_ALL/frame_ALL4.jpg')
    img=cv2.imread('/home/pi/windows_shared/frame_ALL.jpg')
    img ,color1,_  = circle_color(img)
    cube_color_str_dis(color1)
    
    cv2.imshow('img',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()









