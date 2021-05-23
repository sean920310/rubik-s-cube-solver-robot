from subprocess import Popen , PIPE
print('not ok!!!!!!!!!!!')
p = Popen( ['/home/pi/Desktop/rob-twophase-master/twophase' ,'-m 1000'] , stdin=PIPE, stdout=PIPE)
       
while 'Ready!' not in p.stdout.readline().decode():
            pass # wait for everything to boot up

print('ok!!!!!!!!!!!')



def rob_2_phase_solve(face):
    if face == '' or face == ' 'or face == '  'or face == '   ':
        return 'error'
    
    p.stdin.write(('solve %s\n' % face).encode())
    p.stdin.flush()

    tmp = p.stdout.readline().decode()
    sol = p.stdout.readline().decode()
    if 'error' in tmp:
        return 'error'
    
        
        
    #print(tmp)
    #print(sol)
    step = sol.split(' ')[-1]
    sols = ' '.join(sol.split(' ')[:-1]) # delete appended solution length
    print("step =", step)
    print("sols= ",sols)
    p.stdout.readline().decode()
    return sols




if __name__ == '__main__':
    while 1 :
        
        face = input('enter face:  ')
        sols = rob_2_phase_solve(face)
       
        print( sols )




