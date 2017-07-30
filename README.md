# Emotion AI

**Emotion AI** is a small project I completed that identifies a user's facial expressions and emotions and returns song reccommendations based on these emotions. The hardware setup consists of a Raspberry Pi connected to a Pi camera mounted to a camera gimbal of two servos. Microsoft Azure's Cognitive Services is used detect facial emotions in images captured by the camera. When image classification data is retrieved by the Pi, the program will create tags associated with the user's current mood and search Spotify for an appropiate song from different playlists. The Pi camera will also detect, lock-on, and follow the user's face using OpenCV and PID control for the gimbal.

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

Obtain required [Microsoft Azure](https://azure.microsoft.com/en-ca/try/cognitive-services/?api=emotion-api) and [Spotify](https://developer.spotify.com/web-api/) keys and run main.py.
