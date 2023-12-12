import tkinter as tk
from time import strftime
import threading
import speech_recognition as sr
import pyttsx3

def time():
    string = strftime('%H:%M:%S %p')
    time_label.config(text=string)
    time_label.after(1000, time)  # Update every 1000 milliseconds (1 second)

def date():
    string = strftime('%B %d, %Y')
    date_label.config(text=string)

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

def animate_background():
    for _ in range(5):  # Change the background color 5 times
        root.config(bg='lightblue')  # Change the background color to lightblue
        root.update()
        root.after(500)  # Pause for 500 milliseconds
        root.config(bg='white')  # Change the background color back to white
        root.update()
        root.after(500)  # Pause for 500 milliseconds

def main():
    while True:
        command = listen()
        if command:
            if "hey jarvis" in command:
                speak("How can I help you today?")
                # Implement your logic for handling user commands here
                # Trigger the background animation when Jarvis speaks
                threading.Thread(target=animate_background).start()

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
