#!/usr/bin/python

import socket
import sys
import wiringpi
import time
from threading import Thread
import thread
import datetime
import RPi.GPIO as GPIO

global front
global prevFront
global rear
global test
global conn 
global addr
global ready
global inputArray_Front
ready=False
		
front="Neutral"
rear="Neutral"
prevRear="Neutral"
prevFront="Neutral"

global control
global servo
global p

def frontWheelListener(): #külön szál kezeli az első kerék kormányzását
	control = [5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
	servo = 22 #pin
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(servo,GPIO.OUT)
	p=GPIO.PWM(servo,50)
	p.start(2.5)
	
	while(True):
		try:
			if(front=="Left"): #balra
				p.ChangeDutyCycle(5.9)
				time.sleep(0.1)
			else:
				if(front=="Right"): #jobbra
					p.ChangeDutyCycle(9.1)
					time.sleep(0.1)
				else:	
					p.ChangeDutyCycle(7.5)
					time.sleep(0.1)
		except KeyboardInterrupt:
			GPIO.cleanup()
    
wiringpi.wiringPiSetup() #a raspberry pi általunk használt pinjeit "output" cimkével látjuk el
wiringpi.pinMode(0,1)       
wiringpi.pinMode(22,1)
wiringpi.pinMode(23,1)
wiringpi.pinMode(24,1)
wiringpi.pinMode(25,1)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socketet nyitunk
s.connect(('192.0.0.8',1027))
ipAddr=s.getsockname()[0]
print(ipAddr) #kiírjuk az ip címet ami alapján csatlakozunk az autóra
print socket.gethostname()
mySocket = socket.socket()
mySocket.bind((ipAddr,8080))
mySocket.listen(1)	#1 csatlakozást vár

while True:
		try:
			print("Waiting for a connection...")
			conn, addr = mySocket.accept() 
			print("Connection from: "+str(addr))
			thread = Thread(target = frontWheelListener, args = ()) #az első kerék kormányzásához való szál elindul
			thread.start()
			while True:
				data = conn.recv(64)
				if data:
					# a beérkező adatfolyam alapján eldől az irányítás
					if data.find("w")!=(-1):
						rear="Forward"
					else:
						if data.find("s")!=(-1):
							rear="Reverse"
						else:
							rear="Neutral"
					if data.find("a")!=(-1):
						front="Left"
					else:
						if data.find("d")!=(-1):
							front="Right"
						else:
							front="Neutral"
													
						if data.find("o")!=(-1):
							wiringpi.digitalWrite(22,1)
							wiringpi.digitalWrite(23,1)
							wiringpi.digitalWrite(24,1)
							wiringpi.digitalWrite(25,1)
						else:
							if data.find("n")!=(-1):
								wiringpi.digitalWrite(22,0)
								wiringpi.digitalWrite(23,0)
								wiringpi.digitalWrite(24,0)
								wiringpi.digitalWrite(25,0)				
					
					if data.find("x")!=(-1):	#az 'X' egyszerű nyugtajel, ha nem adunk parancsot ez folyamatosan érkezik a kliensről
						#ne csinalj semmit
						
					if(rear=="Forward"):
						wiringpi.digitalWrite(0,1)	
						wiringpi.digitalWrite(2,0) 
					else:
						wiringpi.digitalWrite(0,0)
						wiringpi.digitalWrite(2,1) 
												
				else:
					conn, addr = mySocket.accept() 
		finally:
			print("Connection closed.")
			conn.close()



