#1.Mega PROJECT JARVIS
#import pyttsx3
#pyttsx3.speak("Mega Project 1 Jarvis")
import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import pywhatkit
from google import genai


# 1. Setup your API Key
# Make sure this string is exactly what you got from AI Studio
API_KEY = "---------"

# 2. Initialize the client
client = genai.Client(api_key=API_KEY)

# 🔊 Voice (edge-tts + pygame)
import asyncio
import edge_tts
import pygame
import os
import time

pygame.mixer.init()

async def speak_async(text):
    file = "voice.mp3"
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    await communicate.save(file)

    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(file)

def speak(text):
    asyncio.run(speak_async(text))



def take_command():
            listener=sr.Recognizer()
            with sr.Microphone() as source:
                print('Listening----')
                voice=listener.listen(source)
                print('recognizing---')
                try:
                    command=listener.recognize_google(voice)
                    command=command.lower()
                    print("You said",command)
                    if "jarvis" in command.lower():
                        command=command.replace('Jarvis ','').strip()
                        speak('Yes sir how can i help you')
                    return command
                except:
                    print("Didnt get that")
                    return ""

def ask_ai(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Answer clearly in 1-2 lines: " + user_input
        )

        # 🔥 Try main text
        if hasattr(response, "text") and response.text:
            return response.text

        # 🔥 Fallback (important)
        elif response.candidates:
            return response.candidates[0].content.parts[0].text

        else:
            return "I couldn't understand that properly"

    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong"

take_command()
def run_jarvis():
    command=take_command()
    if "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open whatsapp" in command.lower():
        webbrowser.open("https://web.whatsapp.com/")
    elif "open chatgpt" in command.lower():
        webbrowser.open("https://chatgpt.com/")
    elif "open instagram" in command.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open facebook" in command.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open spotify" in command.lower():
        webbrowser.open("http://spotify.com/")
    elif "play" in command.lower():
        song=command.replace("Play","")
        speak("playing"+ song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is ' + time)
    elif "stop" in command or "exit" in command:
        speak('Goodbye')
        exit()
    elif "ai mode" in command:
        speak("Let me think")
        reply = ask_ai(command)
        print("AI:", reply)
        speak(reply)
    elif command != "":
        # 🔥 automatic AI fallback
        reply = ask_ai(command)
        print("AI:", reply)
        speak(reply)
if __name__=="__main__":
    speak("Initializing Jarvis.....")
    while True:
        run_jarvis()

