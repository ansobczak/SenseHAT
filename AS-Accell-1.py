from pisense import * #SenseHAT, array, draw_text
from colorzero import Color
from random import randint, choice
from time import sleep, time
import datetime
import random										#FOR TEST ONLY

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
bri=2 #brightness



#set temp pixels
Temp_px2 = [ (4,0),(3,0),(2,0),(1,0),(0,0),(4,1),(3,1),(2,1),(1,1),(0,1) ] #list of temperature pixels
Temp_px3 = [ (7,0),(7,1),(6,0),(6,1) ] #list of 10x temperature pixels
VarioPix1 = [(3,2),(2,2),(1,2),(0,2)] #pixels for ascending
VarioPix2 = [(4,2),(5,2),(6,2),(7,2)] #pixels for descending
vcollu=g #vario colors low (for 0-1 m/s) and hi (above 1 m/s) up and down
vcolhu=y
vcolld=d
vcolhd=r
HumPix = [(7,3),(6,3),(5,3),(4,3),(3,3),(2,3),(1,3),(0,3)] #pixels for hunidity

PresPix1 = [(3,4),(2,4),(1,4),(0,4)] #pixels for incresed hunidity
Presix2 = [(4,4),(5,4),(6,4),(7,4)] #pixels for decresed hunidity

gonogo=1 #global flag to control run of procedures in the main loop
Stick_direction="" #global for stick direction

################################################################
################################################################	this should be replaced with real procedures

def ll(t="ll"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,0]=m
	Stick_direction=t
	
def ul(t="ul"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[0,0:8]=m
	Stick_direction=t
	
def rl(t="rl"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,7]=m
	Stick_direction=t
	
def dl(t="dl"):
#	print(t,end="\n")	
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[7,0:8]=m
	Stick_direction=t
		
def el(t="el"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[3:5,3:5]=m
	Stick_direction=t

def lh(t="lh"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,0]=r
	Stick_direction=t

def uh(t="uh"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[0,0:8]=r
	Stick_direction=t

def rh(t="rh"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,7]=r
	Stick_direction=t

def dh(t="dh"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[7,0:8]=r
	Stick_direction=t

def eh(t="eh"):
#	print(t,end="\n")
	global Stick_direction
	hat.screen.array[0:,0:]=b
	hat.screen.array[3:5,3:5]=r
	Stick_direction=t
#	exit()
################################################################
################################################################	

def PrintTemp():
	global w, b,curr_temp
	ShowLetters("T",delay=3, forgrd=w,bckgrd=b)
	ShowLetters(f"{curr_temp:.1f}", delay=6, forgrd=w,bckgrd=b)  #presents current temperature

def PrintPress():
	global w, b,curr_pressure
	ShowLetters("P",delay=3, forgrd=w,bckgrd=b)
	ShowLetters(f"{curr_pressure:.0f}", delay=6, forgrd=w,bckgrd=b)  #presents current presure

def PrintHumi():
	global w, b,curr_humi
	ShowLetters("H",delay=3, forgrd=w,bckgrd=b)
	ShowLetters(f"{curr_humi:.0f}", delay=6, forgrd=w,bckgrd=b)  #presents current presure

def emptyStick():   #empty stick buffer for clear situation reading
    while hat.stick.read(0.001):
        dumb=hat.stick.read


def ShowHumidity(l_hum):
	global HumPix1, HumPix2 #pixels for incresed hunidity
	global y,m,d,s,g,r,w,b,MyScreen	

#	for i in range(8):
#		MyScreen[HumPix[i]]=b #clear humi  pixels

	l_hum=max(10,min(l_hum,100)) #making sure no values outside 10-100 range
	hum_int=int(l_hum) #change to int
	
#	hum_int=random.randint(8, 99) 													#FOR TEST
	
	tc=b #setting color to black just in case something is wrong

	if hum_int in range (40,72): #set colours for humi
		tc=g
	elif hum_int in range (72,100):
	   tc=s
	elif hum_int in range (20,40):
	   tc=m
	elif hum_int in range (0,20):
	   tc=y	   
	for i in range (min(hum_int//10,8)):
			MyScreen[HumPix[i]]=tc #pixel in colour	   
#	elif hum_int in range (0,40):
#		for i in range (hum_int//8):
#			MyScreen[HumPix2[i]]=tc #pixel in colour
	   
	   
def ShowVario(ltipr,ntime,npres): #shows the variometer ltipr 0 last measurement of time and pressure
    #VarioPix1

	global vcollu, vcolhu, vcolld, vcolhd

#      print (ltipr,ntime,npres) #test
#	for i in range(4):
#		MyScreen[VarioPix1[i]]=b #clear vario pixels
#		MyScreen[VarioPix2[i]]=b #clear vario pixels

	dtm=ntime-ltipr[0]
	dtmn=dtm.seconds+dtm.microseconds/1000000 #compute time delta in seconds
	dpr=ltipr[1]-npres   #compute pres differenc

	vario=(dpr/dtmn) #compute vario
#	vario=random.randint(-8, 8)/3 													#FOR TEST

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

	global Temp_px2,Temp_px3
	global y,m,d,s,g,r,w,b,MyScreen

	tc=b 	#setting color to black just in case something is wrong
	lTemp=int(lTemp) #change to int

	if lTemp in range (1,10): #set colours for temperature
		tc=m
	elif lTemp in range (10,20):
	   tc=y
	elif lTemp in range (20, 106):
		tc=r
	elif lTemp in range (-9, 0):
		tc=w
	elif lTemp in range (-19, -9):
		tc=s
	elif lTemp in range (-70, -19):
		tc=d
	if lTemp == 0:
		tc=w
		for i in range(10):
			MyScreen[Temp_px2[i]]=tc #pixel in colour

	lTemp=abs(lTemp)

#	for i1 in range(10): #cleans  temperature area on lcd
#	   MyScreen[Temp_px2[i1]]=b   #set it black
#	for i1 in range(4): #cleans  temperature area on lcd
#		MyScreen[Temp_px3[i1]]=b

	for i in range (lTemp % 10):
		MyScreen[Temp_px2[i]]=tc #pixel in colour



	for i in range (int(lTemp / 10)):
		if i > 3: i = 3
		MyScreen[Temp_px3[i]]=tc #pixel in colour
    

def bright():    #set LED brightness by cycling, valid values are 0,1,2
	global b, y, m, i, s, g, r, w, cl_b
	global bri
	global cl_yv, cl_mv, cl_dv, cl_sv, cl_gv, cl_rv, cl_wv
	global cl_yl, cl_ml, cl_dl, cl_sl, cl_gl, cl_rl, cl_wl
	global cl_y, cl_m, cl_d, cl_s, cl_g, cl_r, cl_w
	global vcollu, vcolhu, vcolld, vcolhd

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
#	print("bright ", bri)

def ShowLetters(lstr, delay=6, forgrd=w,bckgrd=b):  #scrols text but remembers what was before
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


def nopres(t=""):   #proc to do nothing basicly, dumb for reading stick and do nothing if nothing is pressed
	global Stick_direction
	Stick_direction=t

 
def StickMov(lp,up,rp,dp,ep,lh,uh,rh,dh,eh): 

#reads stick movements, need to use with:
# nopres() dummy procedure  and it is good to empty stick bufffer with emptyStick() before use

#parameters are functions to call if pressed left, up, right, down, enter:lp,up,rp,dp,ep,
#if held  left, up, right, down, enter:lh,uh,rh,dh,eh

	stickread=None
	funcToRun=nopres  #set dummy procedure if nothing is pressed

	stickreadN=hat.stick.read(0.1)		#read the stick - wait for 0.1s
	while stickreadN:							#if there is a reading, this clears multi touch/stick movement
		if stickreadN.pressed:
			stickread=stickreadN
		stickreadN=hat.stick.read(0.4) #this is a long time, but if shorter  return shit

	if stickread!=None:		#do the below if stick was in use
		if stickread.pressed and not stickread.held:   #if stick was only pressed and NOT held
			try:
				funcToRun={
					'left':  lp,
					'right': rp,
					'up':    up,
					'down':  dp,
					'enter': ep, 
					}[stickread.direction]               

			except KeyError:  #in case it went wrong
				funcToRun=nopres

		if stickread.held:								#if stick was held
			try:
				funcToRun={
					'left':  lh,
					'right': rh,
					'up':    uh,
					'down':  dh,
					'enter': eh, 
			       }[stickread.direction]

			except KeyError:
				funcToRun=nopres
	funcToRun()                                   #executes functions aplied to stick movement


def QNHsetup():  #set up actual QNH
	global  QNH
	global Stick_direction
	global b, y, m, i, s, g, r, w, cl_b
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
		emptyStick()
		Stick_direction=''
		while not (Stick_direction=='el'):  #loops till middle is pressed to loop to the next digit or end
			StickMov(ll,ul,rl,dl,el,lh,uh,rh,dh,eh)
			hat.screen.draw(ImChar(str(res[seq1]),w,b)) #shows the current digit
			hat.screen.array[0,0:1+seq1] = r  #shows pixel to indicate digit in the sequence
			if Stick_direction == "ul" : #pressed up to add, lops from 0 to 9
				if res[seq1] < 9:
					res[seq1]+=1
				else:
					res[seq1]=0
			elif Stick_direction == "dl" : #pressed down to substruct, lops from 9 to 0
				if res[seq1] > 0:
					res[seq1]-=1
				else:
					res[seq1]=9
	#loop end 

	QNH=0
	for seq1 in range(4): #converts res into QNH
		QNH=QNH+res[seq1]*pow(10,3-seq1)
	strQNH=str(QNH)
	blackscreen()
	ShowLetters("QNH",delay=6, forgrd=w,bckgrd=b)
	ShowLetters(strQNH, delay=6, forgrd=w,bckgrd=b)  #presents current QNH
	
def blackscreen():
	hat.screen.array[0:,0:]=b   #MyScreen is an screen array, here all black
	MyScreen=hat.screen.array     #   blSc - is a black screen	MyScreen=hat.screen.array




#######################

#########################MAIN STARTS HERE


######################

hat=SenseHAT()

emptyStick()
bright()

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
	blackscreen()
	curr_temp=reading.temperature
	curr_pressure=reading.pressure
	curr_humi=reading.humidity
	show_temp(curr_temp)
	ShowHumidity(curr_humi)
	tipr=ShowVario(tipr,datetime.datetime.now(),reading.pressure)

	StickMov(QNHsetup,PrintTemp,PrintPress,PrintHumi,bright,lh,uh,rh,dh,eh)     #    StickMov(ll,ul,rl,dl,el,lh,uh,rh,dh,eh)   
	sleep(0.099)





