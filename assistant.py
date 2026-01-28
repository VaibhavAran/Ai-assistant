import speech_recognition as sr
import pyttsx3
import datetime

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        speak("Sorry, I didn't understand.")
        return ""

speak("Hello Vaibhav, I am your assistant.")

while True:
    command = listen()

    if command == "":
        continue

    if "hello" in command:
        speak("Hello! How can I help you?")

    elif "your name" in command:
        speak("My name is Vaibhav assistant.")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "stop" in command or "exit" in command:
        speak("Goodbye Vaibhav.")
        break
