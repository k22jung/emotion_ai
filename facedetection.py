# PWM Servo Limits
#0.029, 0.0745, 0.12 (pin 12, BCM 18) BASE
#0.098, 0.111, 0.127 (pin 33, BCM 13) TILT

import cv2
import numpy as np
import pigpio
import time
import threading
from emotion import emotion
import spotify

PIN_BASE = 18
PIN_TILT = 13
BASE_LEFT = 0.12
BASE_RIGHT = 0.029
TILT_UP = 0.098
TILT_DOWN = 0.127
INCR_X = 0.0007
INCR_Y = 0.0007
PWMANGLE_PER_PIX = 1e-6
IMAGE_H = 480
IMAGE_W = 640
MID_X = IMAGE_W/2
MID_Y = IMAGE_H/2
TOL_Y = 50 #50
TOL_X = 55 #55
TOL_IMG_STAB_X = 20
Kp = (0.955*7.5328e-6)
Ki = 0
Kd = (0.92*12.87e-5)

_spotify_username = '<my_spotify_username>'

class visionTracker:

        def __init__(self):
		self.pi = pigpio.pi()
		self.curr_PWMx = BASE_RIGHT
		self.curr_PWMy = TILT_UP
		self.err_x = 0;
		self.diff_y = 0;
		self.err_xtotal = 0;
		self.cap = None
		self.emotion = None
		self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 
		self.eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
                self.busy = False
                self.currThread = None

        def initServos(self):
                self.pi.set_mode(PIN_BASE, pigpio.OUTPUT)
                self.pi.set_mode(PIN_TILT, pigpio.OUTPUT)

                self.pi.set_PWM_range(PIN_BASE, 40000)
                self.pi.set_PWM_range(PIN_TILT, 40000)

                self.pi.set_PWM_frequency(PIN_TILT, 50)
                self.pi.set_PWM_frequency(PIN_BASE,50)

		self.pi.set_PWM_dutycycle(PIN_BASE, self.curr_PWMx*40000)
		self.pi.set_PWM_dutycycle(PIN_TILT, self.curr_PWMy*40000)
                return
	
	def initVideo(self):
                self.cap = cv2.VideoCapture(0)
		return
		
	def updatePWM(self, face_x, face_y):
		err_x = MID_X - face_x
		out_tol_x = TOL_X < abs(err_x)

		#This won't reply if tolerance too high
		#Only take an image if the camera isn't currently moving
		at_rest = TOL_IMG_STAB_X > abs(self.err_x - err_x)
                #at_rest = 1

                #self.err_xtotal = err_x + self.err_x + self.err_xtotal # trapezoidal rule 

                corr = Kp*err_x + Kd*(err_x - self.err_x)#+ Ki*self.err_xtotal 
                
		# Move left if possible (camera too far right from face)
		if out_tol_x and at_rest and (self.curr_PWMx + corr) < BASE_LEFT and (self.curr_PWMx + corr) > BASE_RIGHT: 
			self.curr_PWMx += corr
			self.pi.set_PWM_dutycycle(PIN_BASE, self.curr_PWMx*40000)

		# Face too high/low, move camera up/down
		diff_y = MID_Y - face_y
		out_tol_y = TOL_Y < abs(diff_y)
	
		if (diff_y > 0) and out_tol_y and (self.curr_PWMy - INCR_Y) > TILT_UP: 
			self.curr_PWMy -= INCR_Y
			self.pi.set_PWM_dutycycle(PIN_TILT, self.curr_PWMy*40000)
		elif (diff_y < 0) and out_tol_y and (self.curr_PWMy + INCR_Y) < TILT_DOWN:
			self.curr_PWMy += INCR_Y
			self.pi.set_PWM_dutycycle(PIN_TILT, self.curr_PWMy*40000)

		self.err_x = err_x;
			
	def trackFace(self):
		try:
                        ret,img = self.cap.read()
                        cv2.imshow('Key Input', img)                     
                
			while True:

                                # Gets an image frame
                                ret,img = (self.cap).read()
                                k = cv2.waitKey(1) & 0xFF
	
				# Start a thread to fetch and compute emotion and best matching song if 'space' is pressed
                                if k == ord(' ') and not(self.busy):
                                        self.busy = True
                                        cv2.imshow('Key Input', img)
                                        self.currThread = threading.Thread(target=self.getEmotion,args=(img,))
                                        self.currThread.start()
                                elif k == ord('q'):
					# Exits if 'q' pressed
                                        self.cleanup()
                                        break

				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                                # If a face is detected, updates PWM to the face position
				if len(faces) is not 0:
					x = faces[0][0]
					y = faces[0][1]
					w = faces[0][2]
					h = faces[0][3]
					
					# X-axis is positive going right
					# Y-axis is positive going downward
					
					#cv2.rectangle(img, (x,y), (x+w, y+h),(225,0,0), 2)
					#print 'X: ', x,' Y: ', y,' W: ', w,' H: ', h
					
					face_x = x+w/2
					face_y = y+h/2
					self.updatePWM(face_x, face_y)
		
		except KeyboardInterrupt:
			self.cleanup()
			return

        def getEmotion(self, img):
                cv2.imwrite('emotion.jpg', img)
                e = emotion()
                self.emotion = e.processEmotion()
                if self.emotion is not None:
                        spotify.getSong(_spotify_username, self.emotion)
                self.busy = False
                return
                
                
			
	def cleanup(self):
		self.pi.set_PWM_dutycycle(PIN_BASE, 0)
		self.pi.set_PWM_dutycycle(PIN_TILT, 0)
		self.pi.stop()
		self.cap.release()
		return




