from gpiozero import Servo
from time import sleep
import os
import sys
import termios
import tty

def getKey():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
	new[6][termios.VMIN] = 1
	new[6][termios.VTIME] = 0
	termios.tcsetattr(fd, termios.TCSANOW, new)
	key = None
	try:
		key = os.read(fd, 3)
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, old)
	return key

servo1 = Servo(2)
servo2 = Servo(3)
x = 0
y = 0
servo1.value = x
servo2.value = y
sleep(1)

 
try: 
	while True:
		key = getKey()
		if key == 'w':
			y = y - 0.2 
		elif key == 's':
			y = y + 0.2
		elif key == 'd':
			x = x + 0.2
		elif key == 'a':
			x = x - 0.2
		else:
			print("WASD controls \n")
		
		
		if x > 1:
			x = 1;
		elif x < -1:
			x = -1
		if y > 1:
			y = 1
		elif y < -1:
			y = -1
				
			
		servo1.value = y
		servo2.value = x
		sleep(0.5)	
		
except:
	print("Something went wrong")
	
