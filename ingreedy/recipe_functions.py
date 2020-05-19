from bs4 import BeautifulSoup
import requests
import unicodedata
import time
import re
import sys
import pyttsx3
import speech_recognition as sr

def get_recipe():
    source_url = 'https://www.bbcgoodfood.com/recipes/classic-lasagne-0'
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    webpage = requests.get(source_url,headers=headers)
    soup = BeautifulSoup(webpage.content, features="html.parser")

    x = 1
    method = []
    method_str = ""

    for i in soup.find_all("li",{"class":"method__item","itemprop":"recipeInstructions"}):
        for j in i:
            method.append(j.text.strip())
            x += 1

    method_str = " ".join(method)
    return method_str

def recognize_speech_from_mic():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        print("Say Something")
        audio = r.listen(source) 
        text = "error"
        try: 
            text = r.recognize_google(audio) 
            print("you said: " + text)
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_sleep_request():
    user_speech = recognize_speech_from_mic()
    while user_speech.isdigit() == False:
        if user_speech.lower() in ["one", "won"]:
            user_speech = 1
        elif user_speech.lower() in ["two", "to", "too"]:
            user_speech = 2
        elif user_speech.lower() in ["three", "tree", "free"]:
            user_speech = 3
        elif user_speech.lower() in ["four", "for", "fir", "fur"]:
            user_speech = 4
        elif user_speech.lower() in ["five"]:
            user_speech = 5
        elif user_speech.lower() in ["six", "sex"]:
            user_speech = 6
        elif user_speech.lower() in ["seven"]:
            user_speech = 7
        elif user_speech.lower() in ["eight", "ate"]:
            user_speech = 8
        elif user_speech.lower() in ["nine"]:
            user_speech = 9
        elif user_speech.lower() in ["ten"]:
            user_speech = 10
        else:
            speak("Sorry, I didn't catch that. How long do you want me to wait for? Say, for example, 5 for 5 minutes.")

    speak("Sure, I will sleep for " + user_speech + " minutes.")
    for i in range(int(user_speech)):
        print(f"{i + 1}")
        time.sleep(1)
    
    return user_speech