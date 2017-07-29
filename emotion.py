from __future__ import print_function
import time 
import requests
import cv2
import operator
import numpy as np
import json
import picamera
import io
import numpy
import time
import sys
import spotipy
import spotipy.util as util
import json
import random
from contextlib import contextmanager
import os
import spotify

#Grab a key at https://www.microsoft.com/cognitive-services/en-US/subscriptions
_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize?' 
_key = '<my_microsoft_key>'
_spotify_username = '<spotify_username>'
_maxNumRetries = 10


def processRequest( json, data, headers, params ):
    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code != 200 and response.status_code != 201:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()) )

        break

    return response.json()  


# Main ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#source ~/.profile
#workon cv

class emotion:

	def __init__(self):
		self.emotions = None
	def takePic (self):
		stream = io.BytesIO()

		with picamera.PiCamera() as camera:
			camera.resolution = (2592, 1944)
			camera.capture(stream, format='jpeg')

		#Convert the picture into a numpy array
		buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

		#Now creates an OpenCV image
		image = cv2.imdecode(buff, 1)

		#Save the result image
		cv2.imwrite('emotion.jpg',image)
		return

	def processEmotion (self):
		# Load raw image file into memory
		pathToFileInDisk = r'emotion.jpg'
		with open( pathToFileInDisk, 'rb' ) as f:
			data = f.read()

		   
		# Computer Vision parameters
		params = None
                json = None
                
		headers = dict()
		headers['ocp-apim-subscription-key'] = _key
		headers['Content-Type'] = 'application/octet-stream'

		

		result = processRequest( json, data, headers, params )
                
		if len(result):
			faces = 0        
			self.emotions = {'happy': ['happy',0], 'sad': ['sad',0], 'neutral': ['Discover Weekly',0], 'mad': ['metal',0], 'scared': ['halloween scary',0]}

			for face in result:
                            faces += 1
			for key, value in face['scores'].iteritems():
				if key == 'happiness':
					self.emotions['happy'][1] += value
				elif key == 'sadness':
					self.emotions['sad'][1] += value
				elif key == 'neutral':
					self.emotions['neutral'][1] += value
				elif key == 'anger':
					self.emotions['mad'][1] += value
				elif key == 'fear':
					self.emotions['scared'][1] += value

			m = 0
			maxKey = None

                        # Find emotion with max value
			for key, value in self.emotions.iteritems():
				self.emotions[key][1] /= faces
				if (self.emotions[key][1]  > m):
					m = self.emotions[key][1]
					maxKey = key

			print ('\n\nYou are {0}.'.format(maxKey))
                        return self.emotions[maxKey][0]

                print('No faces detected.')
                return None

