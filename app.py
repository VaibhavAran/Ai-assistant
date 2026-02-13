from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import pywhatkit
import threading
import time
import pyautogui

app = Flask(__name__)

# Initialize engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    """Speaks the text using pyttsx3."""
    # Running in a separate thread to avoid blocking Flask
    def _speak():
        try:
            # Re-initialize for the thread if needed, but pyttsx3 usually needs the main loop or careful handling.
            # Simple approach: just say and runAndWait.
            # NOTE: pyttsx3 can be tricky with threads. 
            # If this crashes, we might need a dedicated speech queue.
            local_engine = pyttsx3.init()
            local_engine.setProperty("rate", 170)
            local_engine.say(text)
            local_engine.runAndWait()
        except Exception as e:
            print(f"Error speaking: {e}")

    threading.Thread(target=_speak).start()

def listen_function():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"Error listening: {e}")
            return ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    command = listen_function()
    response_text = ""

    if not command:
        return jsonify({'command': '', 'response': "I didn't catch that. Please try again."})

    if "hello" in command:
        response_text = "Hello! How can I help you today?"
        speak(response_text)

    elif "your name" in command:
        response_text = "I am your advanced web assistant."
        speak(response_text)

    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The time is {time_now}"
        speak(response_text)

    elif "wikipedia" in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            response_text = f"According to Wikipedia: {results}"
            speak("Found it.")
        except Exception:
            response_text = "I couldn't find anything on Wikipedia for that."
            speak(response_text)

    elif "joke" in command:
        joke = pyjokes.get_joke()
        response_text = joke
        speak(joke)

    elif "play" in command:
        song = command.replace("play", "").strip()
        response_text = f"Playing {song} on YouTube."
        speak(response_text)
        pywhatkit.playonyt(song)

    elif "search" in command:
        query = command.replace("search", "").strip()
        response_text = f"Searching Google for {query}."
        speak(response_text)
        pywhatkit.search(query)

    elif "volume up" in command:
        pyautogui.press("volumeup")
        speak("Turning volume up")
        response_text = "Volume increased"

    elif "volume down" in command:
        pyautogui.press("volumedown")
        speak("Turning volume down")
        response_text = "Volume decreased"

    elif "stop" in command or "exit" in command:
        response_text = "Goodbye!"
        speak(response_text)
    
    else:
        response_text = "I'm not sure how to help with that yet."
        speak(response_text)

    return jsonify({'command': command, 'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
