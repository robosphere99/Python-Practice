import speech_recognition as sr
import pyttsx3
import pyautogui
import pytesseract
import cv2
import numpy as np

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function for TTS
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Could not request results from Google Speech Recognition service.")
            return ""

# Function to read the screen area
def read_screen_area(x, y, width, height):
    # Take a screenshot of the defined area
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot_np = np.array(screenshot)

    # Convert screenshot to grayscale
    gray_image = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the grayscale image
    text = pytesseract.image_to_string(gray_image)
    return text

# Function to execute commands
def execute_command(command):
    if "read screen" in command:
        # Define the region of the screen you want to read
        # Example: x=100, y=100, width=300, height=200
        x, y, width, height = 100, 100, 300, 200
        text = read_screen_area(x, y, width, height)
        speak(f"I read the following text: {text}")
    elif "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "your name" in command:
        speak("I am your virtual assistant.")
    elif "time" in command:
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "stop" in command:
        speak("Goodbye!")
        return True
    else:
        speak("I am not sure how to assist with that.")

    return False

# Main loop
if __name__ == "__main__":
    while True:
        command = listen()
        if execute_command(command):
            break
