import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.OUT)
p=GPIO.PWM(8,50)
p.start(2.5)
while True:
	p.ChangeDutyCycle(5.8)
