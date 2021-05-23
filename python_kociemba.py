from kociemba import*
from pipe import rob_2_phase_solve
from dictionary import D

def color_to_face(color):
    separate_color = []
    for  i in range(len(color)):
        separate_color.append(color[i])
        if separate_color[i]=='y':separate_color[i]='U'
        elif separate_color[i]=='r':separate_color[i]='R'
        elif separate_color[i]=='b':separate_color[i]='F'
        elif separate_color[i]=='w':separate_color[i]='D'
        elif separate_color[i]=='o':separate_color[i]='L'
        elif separate_color[i]=='g':separate_color[i]='B'
        else: return 'your data is error'
        #print(separate_color[i])
    result = ''.join(separate_color)
    
    return result
def get_python_kociemba_solve(color_str):
    face = color_to_face(color_str)
    sol = solve(face)
    return sol

def sol_to_cmd(sol):
    
    sol_apt = sol.split(' ')

    for i in range( len(sol_apt) ):
        if '(' in sol_apt[i]:
            sol_apt[i] += ' ' + sol_apt[i+1]


           
    for i in range( len(sol_apt) ):
        if '(' not in sol_apt[i]  and  ')' in sol_apt[i] :
            sol_apt[i] = '@'
    for i in range( len(sol_apt) ):
        for n in range( len(sol_apt) ):
            if '@' in sol_apt[n]:
                sol_apt.remove(sol_apt[n])
                break;
            
    for i in range( len(sol_apt) ):
        print(sol_apt[i])
        
    cmd = ''
    for i in range( len(sol_apt) ):
        cmd = cmd + D[ sol_apt[i] ]
    print(cmd)
    return cmd

def get_rob2_kociemba_solve(color):
    sol = rob_2_phase_solve( color_to_face(color) )
    #cmd = sol_to_cmd(sol)
    #print(cmd)
    return sol


if __name__=='__main__':
    color_str = input("enter color string  :")
    sol = get_python_kociemba_solve(color_str)
    print(sol)
    sol = get_rob2_kociemba_solve(color_str)
    print(sol)
    input('enter:')
'''

sol = solve('RRRDULBBUBFFRRULLBUURRFDURDFFFUDBDDRFLLDLBLLLDUUFBBDFB')
print(sol)
'''