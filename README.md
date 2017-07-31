# Emotion AI

**Emotion AI** is a small project I completed that identifies a user's facial expressions and emotions and returns song recommendations based on these emotions. The hardware setup consists of a Raspberry Pi connected to a Pi camera mounted to a camera gimbal of two servos. Microsoft Azure's Cognitive Services is used detect facial emotions in images captured by the camera. When image classification data is retrieved by the Pi, the program will create tags associated with the user's current mood and search Spotify for an appropriate song from different playlists. The Pi camera will also detect, lock-on, and follow the user's face using OpenCV and PID control for the gimbal.

<p align="center"> 
<img src="https://github.com/k22jung/emotion_ai/blob/master/pi_camera_gimbal.jpg">
</p>

## Dependencies

- [OpenCV 3.2.0](http://opencv.org/releases.html)
- [pigpio](http://abyz.co.uk/rpi/pigpio/download.html)

### Python Packages:
- numPy
- json
- spotipy

## Running

### Hardware Requirements
You will need to obtain a [servo pan & tilt](https://www.creatroninc.com/product/servo-motor-pan-tilt-bracket/) and [servos](https://www.creatroninc.com/product/servo-motor-44kgcm/) which I found here. You will also need a [Pi camera](https://www.creatroninc.com/product/noir-camera-board-for-raspberry-pi/?search_query=Pi+camera&results=12) and an external 4 AA battery pack.

### Software Requirements
Obtain required [Microsoft Azure](https://azure.microsoft.com/en-ca/try/cognitive-services/?api=emotion-api) and [Spotify](https://developer.spotify.com/web-api/) keys and run main.py. 
