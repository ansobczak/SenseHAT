#python procedure StickMov that can be use for stick movement reading

from pisense import * #SenseHAT, array, draw_text
from colorzero import Color
from random import randint, choice
from time import sleep, time
import datetime

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


def ll(t="ll"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,0]=m
	
def ul(t="ul"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[0,0:8]=m
	
def rl(t="rl"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,7]=m
	
def dl(t="dl"):
#	print(t,end="\n")	
	hat.screen.array[0:,0:]=b
	hat.screen.array[7,0:8]=m
	
def el(t="el"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	#hat.screen.array[3:5,3:5]=m
	

def lh(t="lh"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,0]=r

def uh(t="uh"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[0,0:8]=r

def rh(t="rh"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[0:8,7]=r

def dh(t="dh"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[7,0:8]=r

def eh(t="eh"):
#	print(t,end="\n")
	hat.screen.array[0:,0:]=b
	hat.screen.array[3:5,3:5]=r
	exit()
def inv_a():
	global a
	a=0

def ehh():
	global a
	a=1
	while a:
		StickMov(rl,dl,ll,ul,el,lh,uh,rh,dh,inv_a)



def nopres():   #proc to do nothing basicly, dumb for reading stick and do nothing if nothing is pressed
   pass

	

def StickMov(lp,up,rp,dp,ep,lh,uh,rh,dh,eh): 

#reads stick movements, need to use with:
# nopres() dummy procedure  and it is good to empty stick bufffer with 
# emptyStick()

#parameters are functions to call if pressed left, up, right, down, enter:lp,up,rp,dp,ep,
#if held  left, up, right, down, enter:lh,uh,rh,dh,eh

	stickread=None
	funcToRun=nopres  #set dummy procedure if nothing is pressed

	stickreadN=hat.stick.read(0.1)		#read the stick - wait for 0.1s
	while stickreadN:							#if there is a reading, this clears multi touch/stick movement
		if stickreadN.pressed:
			stickread=stickreadN
		stickreadN=hat.stick.read(0.4) #this is a long time, but if shorter this return shit

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

def emptyStick():   #empty stick buffer for clear situation reading
	while hat.stick.read(0.001):
		dumb=hat.stick.read

hat=SenseHAT()
hat.screen.array[0:,0:]=b
n=0
emptyStick()
for reading in hat.environ:
	n+=1
	print("      temp  %2.2f %d" % (reading.temperature,n),end="\r")
	StickMov(ll,ul,rl,dl,el,lh,uh,rh,dh,eh)

