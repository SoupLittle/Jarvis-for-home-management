import speech_recognition as sr
import pyttsx3
import tkinter as tk
from time import strftime

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Hey Jarvis'...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        if "hey jarvis" in command:
            return True
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    
    return False

def main():
    while True:
        if listen():
            speak("How can I help you today?")

            # Implement your logic for handling user commands here

if __name__ == "__main__":
    main()
    
def time():
    string = strftime('%H:%M:%S %p')
    time_label.config(text=string)
    time_label.after(1000, time)  # Update every 1000 milliseconds (1 second)

def date():
    string = strftime('%B %d, %Y')
    date_label.config(text=string)

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
root.mainloop()

