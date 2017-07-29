import cv2
import numpy as np
import pigpio
import time
from facedetection import visionTracker
 

eye = visionTracker()


eye.initServos()
eye.initVideo()
eye.trackFace()

