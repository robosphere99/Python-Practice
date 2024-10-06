import speech_recognition as sr
import pyttsx3

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

# Function to execute commands
def execute_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "your name" in command:
        speak("I am your virtual assistant.")
    elif "time" in command:
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}.")
    elif "weather" in command:
        speak("I can't fetch weather updates right now, but you can check a weather app.")
    else:
        speak("I am not sure how to assist with that.")

# Main loop
if __name__ == "__main__":
    while True:
        command = listen()
        execute_command(command)

        if "stop" in command:
            speak("Goodbye!")
            break
