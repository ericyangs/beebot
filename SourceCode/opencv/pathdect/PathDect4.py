#coding:utf-8
#Python中声明文件编码的注释，编码格式指定为utf-8
from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading
import cv2
import numpy as np

print '....WIFIROBOTS START!!!...'

global x
x = 320
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
########LED口定义#################
LED0 = 10
LED1 = 9
LED2 = 25

########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

#########led初始化为000##########
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)


#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000) 
ENA_pwm.start(0) 
ENA_pwm.ChangeDutyCycle(80)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)

GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000) 
ENB_pwm.start(0) 
ENB_pwm.ChangeDutyCycle(80)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
##########机器人方向控制###########################
def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#LED1亮
	GPIO.output(LED2,False)#LED1亮
	
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,True)#LED1灭
	GPIO.output(LED2,False)#LED2亮
	
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,False)#LED1亮
	GPIO.output(LED2,True) #LED2灭
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)#LED1亮
	GPIO.output(LED2,True) #LED2灭
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	GPIO.output(LED1,True)#LED1灭
	GPIO.output(LED2,True)#LED2亮

##########机器人速度控制###########################
def ENA_Speed(EA_num):
	speed=hex(eval('0x'+EA_num))
	speed=int(speed,16)
	print 'EA_A改变啦 %d '%speed
	ENA_pwm.ChangeDutyCycle(speed)

def ENB_Speed(EB_num):
	speed=hex(eval('0x'+EB_num))
	speed=int(speed,16)
	print 'EB_B改变啦 %d '%speed
	ENB_pwm.ChangeDutyCycle(speed)	

def PathDect(func):
	global x
	
	while True:
		if x < 260:
			print("turn left")
			Motor_TurnLeft()
		elif x> 420:
			print("turn right")
			Motor_TurnRight()
		else :
			print("go stright")
			Motor_Forward()
		time.sleep(0.007)
		Motor_Stop()
		time.sleep(0.007)

cap = cv2.VideoCapture(0)

i = 0
x_sum = 0
count = 0
threads = []
t1 = threading.Thread(target=PathDect,args=(u'监听',))
threads.append(t1)

for t in threads:
		t.setDaemon(True)
		t.start()
while True:
	i+=1
	ret,frame = cap.read()	#capture frame_by_frame
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	ret,thresh1=cv2.threshold(gray,70,255,cv2.THRESH_BINARY)
	#if i == 2:
	for j in range(0,640,5):
		if thresh1[240,j] == 0:		
			x_sum = x_sum + j
			count = count + 1
	x = x_sum>>5
	x_sum = 0
	i = 0
	count = 0
	if cv2.waitKey(1)&0XFF ==ord('q'):
		Motor_Stop()
		break
	
cap.relese()
cv2.destroyAllWindows()

