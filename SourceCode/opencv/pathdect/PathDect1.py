import cv2
import numpy as np
cap = cv2.VideoCapture(0)
kernel = np.ones((5,5),np.uint8)
i = 0
x_sum = 0
count = 0
while True:
	i+=1
	ret,frame = cap.read()	#capture frame_by_frame
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	ret,thresh1=cv2.threshold(gray,70,255,cv2.THRESH_BINARY)
	#cv2.rectangle(thresh1,(0,0),(210,480),100,1)
	#cv2.rectangle(thresh1,(210,0),(420,480),100,1)
	#cv2.rectangle(thresh1,(420,0),(640,480),100,1)

	#cv2.rectangle(thresh1,(260,0),(380,480),100,1)
	#cv2.line(thresh1,(210,0),(210,480),180,1)
	#cv2.line(thresh1,(420,0),(420,480),180,1)

	#cv2.line(thresh1,(20,240),(620,240),180,1)
	#thresh1[200,200] = 100
	if i == 1:
		for j in range(0,640,5):
			if thresh1[240,j] == 0:		
				x_sum = x_sum + j
				count = count + 1
		x = x_sum>>5
		#print x
		if x < 	260:
			print("turn left")
		elif x> 420:
			print("turn right")
		else :
			print("go stright")	
		x_sum = 0
		i = 0
		count = 0
	#	pix = thresh1[482,240]
	#	print pix
	

	#cv2.imshow('can_img',thresh1)
#	cv2.imshow('fushi',fushi)
	if cv2.waitKey(1)&0XFF ==ord('q'):
		break
cap.relese()
cv2.destroyAllWindows()
