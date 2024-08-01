from picamera2 import Picamera2

import cv2
import os
import ssl
import time
from datetime import datetime
from src import audio_functions as audio
from src import screenshot_functions as screenshot

import subprocess

from openai import OpenAI

client = OpenAI(api_key="API_KEY")

MODEL="gpt-4o"

audio_filename = "audiodescription.mp3"

#time.sleep(5)

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

    if screenshot.is_image_dark(cropped_image):
        audio.play_mp3("sounds/capturando.mp3")    	
        captureTrigger = True
        continue

    if captureTrigger == False:
        time.sleep(1)
        continue
    else:
        captureTrigger = False	 

    # Convert the OpenCV image to a base64 encoded string
    base64_string = screenshot.convert_cv2_to_base64(cropped_image)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."},
            {"role": "user", "content": [
            {"type": "text", "text": "Please describe this image."},
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

    audio.text_to_speech(text, filenamem)

    audio.play_mp3(filenamem)

picam2.stop()

