import tkinter as tk
from time import strftime
import threading
import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import firebase_admin
from firebase_admin import credentials, storage
from transformers import pipeline

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\Marlene\\Desktop\\Utvikling-hjemme\\Private Jarvis\\Jarvis\\jarvis-6654a-firebase-adminsdk-1gz3o-ea2a000f25.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://jarvis-6654a.appspot.com'
})

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='6e94e305d7904c2abe520e7919ab8ff1',
                                               client_secret='5e69e14d3a7642fb886a8e59da60e3ad',
                                               redirect_uri='https://souplittle.github.io/Jarvis-for-home-management/',
                                               scope='user-read-playback-state,user-modify-playback-state'))

def time():
    current_time = strftime('%H:%M:%S %p')
    time_label.config(text=current_time)
    time_label.after(1000, time)  # Update every 1000 milliseconds (1 second)

def date():
    current_date = strftime('%B %d, %Y')
    date_label.config(text=current_date)
    
    
    # Main Jarvis voice and listen

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Hey Jarvis'...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, could not understand audio.")
            return None
        except sr.RequestError as e:
            speak(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def answer_question(question):
    qa_pipeline = pipeline("question-answering")
    answer = qa_pipeline(question=question, context="Placeholder context. You can replace this.")
    return answer['answer']

def upload_file(local_path, destination_path):
    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(local_path)

def download_file(destination_path, local_path):
    bucket = storage.bucket()
    blob = bucket.blob(destination_path)
    blob.download_to_filename(local_path)

def handle_command(command):
    if "hey jarvis" in command:
        speak("How can I help you today?")
        user_question = listen()
        if user_question:
            if "what is the time" in user_question:
                current_time = strftime('%H:%M:%S %p')
                speak(f"The current time is {current_time}")
            elif "what is the date" in user_question:
                current_date = strftime('%B %d, %Y')
                speak(f"Today's date is {current_date}")
            elif "What is my name?" in user_question:
                speak(f"Your name is Marlene.")
            else:
                # For other questions, use the question-answering pipeline
                answer = answer_question(user_question)
                speak(answer)





# Define functions for the functions


def control_lights():
    speak("Turning on the lights.")

def control_music():
    speak("Playing your favorite music.")

def control_devices():
    speak("Controlling smart devices.")

def main():
    while True:
        command = listen()
        if command:
            handle_command(command)
            
            
            

# Create the main window
root = tk.Tk()
root.title("Hey Jarvis")

# Create and configure labels for time and date
time_label = tk.Label(root, font=('calibri', 40, 'bold'), background='black', foreground='white')
date_label = tk.Label(root, font=('calibri', 20, 'bold'), background='black', foreground='white')

# Create buttons for additional functionalities
lights_button = tk.Button(root, text="Control Lights", command=control_lights)
music_button = tk.Button(root, text="Play Music", command=control_music)
devices_button = tk.Button(root, text="Control Devices", command=control_devices)

# Organize the layout using grid manager
time_label.grid(row=0, column=0, pady=10)
date_label.grid(row=1, column=0, pady=10)
lights_button.grid(row=2, column=0, pady=10)
music_button.grid(row=3, column=0, pady=10)
devices_button.grid(row=4, column=0, pady=10)

# Run the time and date functions
time()
date()

# Start the main loop
root.mainloop()
