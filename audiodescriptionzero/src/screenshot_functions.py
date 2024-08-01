import base64
import cv2 
import numpy as np

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