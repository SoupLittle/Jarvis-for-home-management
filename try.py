import tkinter as tk
from time import strftime
import threading
import speech_recognition as sr
import pyttsx3
from transformers import pipeline

def time():
    current_time = strftime('%H:%M:%S %p')
    time_label.config(text=current_time)
    time_label.after(1000, time)  # Update every 1000 milliseconds (1 second)

def date():
    current_date = strftime('%B %d, %Y')
    date_label.config(text=current_date)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Hey Jarvis'...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def answer_question(question):
    qa_pipeline = pipeline("question-answering")
    answer = qa_pipeline(question=question, context="Placeholder context. You can replace this.")
    return answer['answer']

def handle_command(command):
    if "hey jarvis" in command:
        speak("How can I help you today?")
        user_question = listen()
        if user_question:
            if "what is the time" in user_question:
                current_time = strftime('%H:%M:%S %p')
                speak(f"The current time is {current_time}")
            else:
                # For other questions, use the question-answering pipeline
                answer = answer_question(user_question)
                speak(answer)

def main():
    while True:
        command = listen()
        if command:
            handle_command(command)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("Hey Jarvis")

    # Create and configure labels for time and date
    time_label = tk.Label(root, font=('calibri', 40, 'bold'), background='black', foreground='white')
    date_label = tk.Label(root, font=('calibri', 20, 'bold'), background='black', foreground='white')

    # Pack the labels into the main window
    time_label.pack(anchor='center')
    date_label.pack(anchor='center')

    # Run the time and date functions
    time()
    date()

    # Start the main loop
    root.after(0, main)  # Run the main function after 0 milliseconds
    root.mainloop()
