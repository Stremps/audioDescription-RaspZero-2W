from picamera2 import Picamera2

import cv2
import numpy as np

import base64
import os
import ssl
import time
from datetime import datetime

import subprocess

from openai import OpenAI

client = OpenAI(api_key="API_KEY")

MODEL="gpt-4o"

audio_filename = "audiodescription.mp3"

#time.sleep(5)

def play_mp3(file_path):
    try:
        subprocess.run(['mpg123', file_path])
    except FileNotFoundError:
        print("mpg123 command not found. Make sure you're on macOS and afplay is installed.")

def text_to_speech(text, filename):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(filename)

def convert_cv2_to_base64(cv2_image):
    """
    Convert an OpenCV image to a base64 encoded string.
    
    :param cv2_image: OpenCV Image (numpy array)
    :return: Base64 encoded string of the image
    """
    # Encode the image to a buffer
    _, buffer = cv2.imencode('.png', cv2_image)
    
    # Convert the buffer to a base64 string
    base64_string = base64.b64encode(buffer).decode('utf-8')
    
    return base64_string

def is_image_dark(image, threshold=50):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate the mean brightness
    mean_brightness = np.mean(gray_image)
    
    # Determine if the image is dark
    is_dark = mean_brightness < threshold
    
    return is_dark

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (800, 600)})
picam2.configure(config)

picam2.start()

captureTrigger = False

while True:

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create filenames with the timestamp
    filenamej = f"data/{timestamp}.jpg"
    filenamet = f"data/{timestamp}.txt"
    filenamem = f"data/{timestamp}.mp3"

    picam2.capture_file("input.jpg")
    
    cropped_image = cv2.imread("input.jpg")
    cv2.imwrite(filenamej, cropped_image)

    if is_image_dark(cropped_image):
        play_mp3("capturando.mp3")    	
        captureTrigger = True
        continue

    if captureTrigger == False:
        time.sleep(1)
        continue
    else:
        captureTrigger = False	 

    # Convert the OpenCV image to a base64 encoded string
    base64_string = convert_cv2_to_base64(cropped_image)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a person that provides professional audio description services for blind people. Help me describe the images I show you in Brazilian portuguese."},
            {"role": "user", "content": [
            {"type": "text", "text": "Please describe this image focusing in aiding locomotion for a blind person. I want to know if the way ahead is free for walking. Describe the scene to help me to walk with more confidence, knowing if there is any obstacle in front of me. Be brief, i want a short sentence telling me only the necessary to step foward."},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_string}"}
                }
            ]}
        ],
        temperature=0.0,
        )

    text = response.choices[0].message.content

    print(text)

    

    with open(filenamet, 'w') as file:
        file.write(text)

    text_to_speech(text, filenamem)

    play_mp3(filenamem)

picam2.stop()

