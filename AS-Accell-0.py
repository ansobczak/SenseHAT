from pisense import * #SenseHAT, array, draw_text
from colorzero import Color
from random import randint, choice
from time import sleep, time
import datetime

#set up colors
cl_y = Color.from_rgb_bytes(255, 255, 0)  #bright  #yellow
cl_yl = Color.from_rgb_bytes(100, 100, 0) #dim
cl_yv= Color.from_rgb_bytes(55, 55, 0) #more dim
cl_m = Color.from_rgb_bytes(0,255,255)               #light blue / 
cl_ml = Color.from_rgb_bytes(0,100, 100)
cl_mv = Color.from_rgb_bytes(0,55,55)
cl_d = Color.from_rgb_bytes(255,0,255)                    #indygo
cl_dl = Color.from_rgb_bytes(100,0,100)
cl_dv = Color.from_rgb_bytes(55,0,55)
cl_s = Color.from_rgb_bytes(0,0,255)  #s like the Sky is blue  #blue
cl_sl = Color.from_rgb_bytes(0,0,120)
cl_sv = Color.from_rgb_bytes(0,0, 55)
cl_g = Color.from_rgb_bytes(0,255,0)                    #green
cl_gl = Color.from_rgb_bytes(0,105,0)
cl_gv = Color.from_rgb_bytes(0,55,0)
cl_r = Color.from_rgb_bytes(255, 0,0)                     #red
cl_rl = Color.from_rgb_bytes(155, 0,0)
cl_rv = Color.from_rgb_bytes(55, 0,0)
cl_w = Color.from_rgb_bytes(255, 255, 255)           #white
cl_wl = Color.from_rgb_bytes(105, 105, 105)
cl_wv = Color.from_rgb_bytes(55, 55,55)
cl_b = Color.from_rgb_bytes(0, 0,0) #black is always black
 #just initiate
y=cl_y #bright  #yellow
m=cl_m #light blue
d=cl_d #indygo
s=cl_s #s like the Sky is blue  #blue
g=cl_g #green
r=cl_r #red
w=cl_w #white
b=cl_b   #black is always black
bri=1 #brightness



#set temp pixels
Temp_px2 = [ (4,0),(3,0),(2,0),(1,0),(0,0),(4,1),(3,1),(2,1),(1,1),(0,1) ] #list of temperature pixels
Temp_px3 = [ (7,0),(7,1),(6,0),(6,1) ] #list of 10x temperature pixels
VarioPix1 = [(3,2),(2,2),(1,2),(0,2)] #pixels for ascending
VarioPix2 = [(4,2),(5,2),(6,2),(7,2)] #pixels for descending
vcollu=g #vario colors low (for 0-1 m/s) and hi (above 1 m/s) uo and down
vcolhu=y
vcolld=d
vcolhd=r
HumPix1 = [(3,2),(2,2),(2,2),(0,2)] #pixels for ascending
HumPix2 = [(4,2),(5,2),(6,2),(7,2)] #pixels for descending

gonogo=1 #global flag to control run of procedures in the main loop

def emptyStick():   #empty stick buffer for clear situation reading
    while hat.stick.read(0.001):
        dumb=hat.stick.read

def ShowVario(ltipr,ntime,npres): #shows the variometer ltipr 0 last measurement of time and pressure
    #VarioPix1
    global gonogo
    global vcollu, vcolhu, vcolld, vcolhd
    if gonogo==1:
#      print (ltipr,ntime,npres) #test
      for i in range(4):
        MyScreen[VarioPix1[i]]=b #clear vario pixels
        MyScreen[VarioPix2[i]]=b #clear vario pixels

      dtm=ntime-ltipr[0]
      dtmn=dtm.seconds+dtm.microseconds/1000000 #compute time delta in seconds
      dpr=ltipr[1]-npres   #compute pres differenc

      vario=(dpr/dtmn) #compute vario

#      print(dtmn,dpr, vario)  #test
      if abs(vario) > 0.1 and abs(vario) < 1:  #if vario in <-1,1> change colors and scale, showing 1/4 m/s in green up and indigo down
        vario=vario*4+1
        vcu=vcollu
        vcd=vcolld
      else:
        vcu=vcolhu #colors setup yellow up and red down
        vcd=vcolhd 

      vario=int(vario)
      vario=max(-4,min(vario,4)) #clump to pixels

      for i in range (vario):
        MyScreen[VarioPix1[i]]=vcu #pixel in colour
      if vario < 0:
        vario=abs(vario)
        for i in range (vario):
          MyScreen[VarioPix2[i]]=vcd #pixel in colour
    return([ntime,npres])




def show_temp(lTemp):   #display temperature in pixels Tpix1, Tpix2

  global gonogo,Temp_px2,Temp_px3
  if gonogo==1:
    global y,m,d,s,g,r,w,b,MyScreen
    for i1 in range(10): #cleans  temperature area on lcd
      MyScreen[Temp_px2[i1]]=b   #set it black
    for i1 in range(4): #cleans  temperature area on lcd
      MyScreen[Temp_px3[i1]]=b

    lTemp=int(lTemp) #change to int
#    print(lTemp)
    if lTemp in range (1,10): #set colours for temperature
      tc=m
#      print("x1-16")
    elif lTemp in range (10,20):
      tc=y
#      print("X16")
    elif lTemp in range (20, 106):
      tc=r
#      print("X+20")
    elif lTemp in range (-9, 0):
      tc=w
#      print("X-10")
    elif lTemp in range (-19, -9):
      tc=s
 #     print("X-20")
    elif lTemp in range (-70, -19):
      tc=d
#      print("X-70")
    if lTemp == 0:
      tc=w
      for i in range(10):
        MyScreen[Temp_px2[i]]=tc #pixel in colour
    lTemp=abs(lTemp)
    for i in range (lTemp % 10):
      MyScreen[Temp_px2[i]]=tc #pixel in colour
    for i in range (int(lTemp / 10)):
      if i > 3: i = 3
      MyScreen[Temp_px3[i]]=tc #pixel in colour
    

def bright(event):    #set LED brightness by cycling, valid values are 0,1,2
    global b, y, m, i, s, g, r, w, cl_b
    global bri
    global cl_yv, cl_mv, cl_dv, cl_sv, cl_gv, cl_rv, cl_wv
    global cl_yl, cl_ml, cl_dl, cl_sl, cl_gl, cl_rl, cl_wl
    global cl_y, cl_m, cl_d, cl_s, cl_g, cl_r, cl_w
    global vcollu, vcolhu, vcolld, vcolhd
    print("bright ", bri )
#    if True: # in ('pressed'):    
    if event.pressed and not event.held:
      b=cl_b   #black is always black
      bri+=1
      if bri not in (0,1,2):
        bri=0
      if bri == 0:
        y=cl_yv
        m=cl_mv
        d=cl_dv
        s=cl_sv
        g=cl_gv
        r=cl_rv
        w=cl_wv
      elif bri == 1:
        y=cl_yl
        m=cl_ml
        d=cl_dl
        s=cl_sl
        g=cl_gl
        r=cl_rl
        w=cl_wl
      elif bri == 2:
        y=cl_y
        m=cl_m
        d=cl_d
        s=cl_s
        g=cl_g
        r=cl_r
        w=cl_w
      vcollu=g #vario colors low (for 0-1 m/s) and hi (above 1 m/s) uo and down
      vcolhu=y
      vcolld=d
      vcolhd=r
    else: print('bright else')

def  ShowLetters(lstr, delay=6, forgrd=w,bckgrd=b):  #scrols text but remembers what was before
    CpScreen=hat.screen.array.copy()
    #print(lstr,delay,forgrd)
    hat.screen.scroll_text(text=lstr,duration=delay, foreground=forgrd,background=bckgrd)
    hat.screen.array=CpScreen

def ShowChar(lstr, delay=6, forgrd=w,bckgrd=b):  #displays single char but remembers what was before
    CpScreen=hat.screen.array.copy()
    im=draw_text(" "+lstr+" ",foreground=forgrd, background=bckgrd)
    ar=array(im)
    a8=ar[:8,2:10]
    #a8.show()
    imm=buf_to_image(a8)
    hat.screen.draw(imm)
    sleep(delay)
    hat.screen.array=CpScreen

def ImChar(lstr, forgrd=w,bckgrd=b): #prepares array with single character
    im=draw_text(" "+lstr+" ",foreground=forgrd, background=bckgrd)    
    ar=array(im)
    a8=ar[:8,2:10]
    #a8.show()
    imm=buf_to_image(a8)
    return imm
 
def StickMov(events): #reads stick movements
    for event in events:
        print("    V    ")
        
        if event.held and event.direction=='enter':
            print("enter")
            try:
                yield {
#                    'left':  (-2, 0),
#                    'right': (2, 0),
#                    'up':    (0, -2),
#                    'down':  (0, 2),
                    'enter': (-2,-2),
                    }[event.direction]
#            break  # enter exits
            except KeyError:
                break  # enter exits

        elif event.pressed:
            print("P", event)
            try:
                yield {
                    'left':  (-1, 0),
                    'right': (1, 0),
                    'up':    (0, -1),
                    'down':  (0, 1),
                    'enter': (-1,-1),
                }[event.direction]
            except KeyError:
                break  # enter exits
        else:
            print("E")


def QNHsetup(event):  #set up actual QNH
    global gonogo, QNH
    gonogo=0
    res=[0,0,0,0] #results are stored here
    MyScreen[0:,0:]=b   #set screen to blank
#    sense.set_rotation() 

    strQNH=str(QNH)
    if len(strQNH) == 3:  #if QNH is 3 digit long, add 0 at front
      strQNH="0"+strQNH

    ShowLetters("QNH",delay=6, forgrd=w,bckgrd=b)
    ShowLetters(strQNH, delay=6, forgrd=w,bckgrd=b)  #presents current QNH
    
    for seq1 in range(len(strQNH)): #loops for each digit
      res[seq1]=int(strQNH[seq1]) #set result equal to actual value

      hat.screen.draw(ImChar(str(res[seq1]),w,b)) #shows the current digit
      hat.screen.array[0,0:1+seq1] = r  #shows pixel to indicate digit in the sequence
      sleep(2)
      
      
#    event = hat.stick.wait_for_event(emptybuffer=True)
    emptyStick()
    event=hat.stick.read()
    while not (event.direction=='middle' and event.action == "pressed"):  #loops till middle is pressed to loop to the next digit or end
        
        if event.direction == "up" and event.action == "released": #pressed up to add, lops from 0 to 9
            if res[seq1] < 9:
            res[seq1]+=1
        else:
            res[seq1]=0
        elif event.direction == "down" and event.action == "released": #pressed down to substruct, lops from 9 to 0
            if res[seq1] > 0:
            res[seq1]-=1
        else:
          res[seq1]=9
        #print("QNH", QNH, strQNH, res) #test
        ShowChar(str(res[seq1])) #shows current digit
        sense.set_pixel(seq1, 0, r)   #shows digit sequence (tousend, houndreds and so on)
#        event = sense.stick.wait_for_event()
        event=hat.stick.read()
        #print("QNH", QNH, strQNH, res) #test
    QNH=0
    for seq1 in range(4): #converts res into QNH
      QNH=QNH+res[seq1]*pow(10,3-seq1)
    #loop end  
    #print("QNH", QNH, strQNH, res)#test

    ShowLetters("QOK", 0.3)
    strQNH=str(QNH)
    ShowLetters(strQNH, 0.7)  #presents current QNH   
    gonogo=1
        




#######################

#########################MAIN STARTS HERE


######################

hat=SenseHAT()


QNH=1002 #initate QNH
tipr=[datetime.datetime.now(),hat.environ.pressure]  #this is start data for Vario - time and pressure
#print(s_press, s_Temp, Altm, Altf, "QNH:",QNH) #for testing

hat.screen.array[0:,0:]=b   #MyScreen is an screen array, here all black
MyScreen=hat.screen.array     #   blSc - is a black screen
hat.screen.rotation=0
#### OK     hat.stick.when_up = QNHsetup
#sense.stick.direction_down = prt_Alt
#sense.stick.direction_left = prt_temp
#### OK     hat.stick.when_right = bright
#sense.stick.direction_middle = led_cln


for reading in hat.environ:
    show_temp(reading.temperature)
    tipr=ShowVario(tipr,datetime.datetime.now(),reading.pressure)
    StickMov(hat.stick)     
    sleep(0.099)





