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
inputArray_Front=['x','x','x','x','x','x','x','x','x','x'] 	

global control
global servo
global p

def putInArray(c):
	for i in range(0,9):
		inputArray_Front[i]=inputArray_Front[i+1]
	inputArray_Front[9]=c

def evaluate(c):
	value=0
	for i in range(0,10):
		if inputArray_Front[i]==c:
			value+=1
	return value
	

def frontWheelListener():
	control = [5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
	servo = 14 #pin
	GPIO.setup(servo,GPIO.OUT)
	p=GPIO.PWM(servo,50)
	p.start(2.5)
	
	while(True):
		try:
			if(front=="Left"): #balra
				p.ChangeDutyCycle(5.8)
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

time.sleep(10)			

wiringpi.wiringPiSetup()
wiringpi.pinMode(0,1)       
wiringpi.pinMode(22,1)
wiringpi.pinMode(23,1)
wiringpi.pinMode(24,1)
wiringpi.pinMode(25,1)
wiringpi.pinMode(27,1)

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
rear_p=GPIO.PWM(en,1000)

rear_p.start(25)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('192.0.0.8',1027))
ipAddr=s.getsockname()[0]
print(ipAddr)
print socket.gethostname()
mySocket = socket.socket()
mySocket.bind((ipAddr,8080))
mySocket.listen(1)

GPIO.setup(22,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.output(22,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
while True:
		try:
			print("Waiting for a connection...")
			conn, addr = mySocket.accept() 
			print("Connection from: "+str(addr))
			thread = Thread(target = frontWheelListener, args = ())
			thread.start()
			while True:
				data = conn.recv(64)
				if data:
					if data.find("0")!=(-1):
						rear_p.ChangeDutyCycle(5)
						putInArray('x')
					elif data.find("1")!=(-1):
						rear_p.ChangeDutyCycle(10)
						putInArray('x')
					elif data.find("2")!=(-1):
						rear_p.ChangeDutyCycle(20)
						putInArray('x')
					elif data.find("3")!=(-1):
						rear_p.ChangeDutyCycle(30)
						putInArray('x')
					elif data.find("4")!=(-1):
						rear_p.ChangeDutyCycle(40)
						putInArray('x')
					elif data.find("5")!=(-1):
						rear_p.ChangeDutyCycle(50)
						putInArray('x')
					elif data.find("6")!=(-1):
						rear_p.ChangeDutyCycle(60)
						putInArray('x')
					elif data.find("7")!=(-1):
						rear_p.ChangeDutyCycle(70)
						putInArray('x')
					elif data.find("8")!=(-1):
						rear_p.ChangeDutyCycle(80)
						putInArray('x')
					elif data.find("9")!=(-1):
						rear_p.ChangeDutyCycle(90)
						putInArray('x')
					elif data.find("n")!=(-1):
						rear_p.ChangeDutyCycle(100)
						putInArray('x')
						
					if data.find("w")!=(-1):
						rear="Forward"
					else:
						if data.find("s")!=(-1):
							rear="Reverse"
						else:
							rear="Neutral"
					if data.find("a")!=(-1):
						putInArray('a')
						if evaluate('a')>=1:
							front="Left"
					else:
						if data.find("d")!=(-1):
							front="Right"
							putInArray('d')
						else:
							if evaluate('a')==0 and evaluate('d')==0:
								front="Neutral"
						if data.find("q")!=(-1):
							GPIO.output(22,GPIO.HIGH)
							GPIO.output(27,GPIO.HIGH)
							time.sleep(0.3)
							GPIO.output(22,GPIO.LOW)
							GPIO.output(27,GPIO.LOW)
							time.sleep(0.3)
							GPIO.output(22,GPIO.HIGH)
							GPIO.output(27,GPIO.HIGH)
							time.sleep(0.3)
							GPIO.output(22,GPIO.LOW)
							GPIO.output(27,GPIO.LOW)
							time.sleep(0.3)
							GPIO.output(22,GPIO.HIGH)
							GPIO.output(27,GPIO.HIGH)
							command = "/usr/bin/sudo /sbin/shutdown 0"
							import subprocess
							process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
							output = process.communicate()[0]
							
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
												
					if(rear=="Forward"):
						GPIO.output(in1,GPIO.LOW)
						GPIO.output(in2,GPIO.HIGH)
						putInArray('w')
					elif(rear=="Reverse"):
						GPIO.output(in1,GPIO.HIGH)
						GPIO.output(in2,GPIO.LOW)
						putInArray('s')
					else:
						GPIO.output(in1,GPIO.LOW)
						GPIO.output(in2,GPIO.LOW)
												
				else:
					conn, addr = mySocket.accept() 
		finally:
			print("Connection closed.")
			conn.close()

