from bs4 import BeautifulSoup
import requests
import unicodedata
import time
import re
import sys
import pyttsx3
import speech_recognition as sr
from recipe_functions import get_recipe, recognize_speech_from_mic, speak

# -------------------------------------------------------------
# Good webpage for JavaScript speech
# https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API/Using_the_Web_Speech_API
# -------------------------------------------------------------

def main():
    method_str = get_recipe()
    print(method_str)

    split_recipe_sentences = method_str.split(".")
    recipe_instructions = []

    for sentence in split_recipe_sentences:
        x = sentence.replace(u'\xa0', u' ')
        if sentence != '':
            recipe_instructions.append(x.strip())

    sentence_id = 0
    recipe_schedule = []
    time_amt, time_unit = '', ''

    for sentence in recipe_instructions:
        recipe_item = {}

        word_split = re.split(r'[-,\.\s]', sentence)
        
        i, for_cnt, for_idx, time_unit_idx = 0, 0, 0, 0

        for word in word_split:
            if word.lower() == "about":
                if word_split[i-1] == "for":
                    word_split.remove(word)
            if word.lower() == "for":
                for_idx =  i
                for_cnt += 1
                if for_cnt == 2:
                    exit('more than 2 fors in a sentence')

            if word.lower().startswith(('sec', 'min', 'hour', 'hr')): 
                if word.lower().startswith("s"):
                    if word.lower().endswith("s"):
                        time_unit = "seconds"
                    else:
                        time_unit = "second"
                elif word.lower().startswith("m"):
                    if word.lower().endswith("s"):
                        time_unit = "minutes"
                    else:
                        time_unit = "minute"
                elif word.lower().startswith("h"):
                    if word.lower().endswith("s"):
                        time_unit = "hours"
                    else:
                        time_unit = "hour"  
                else:
                    exit("what time unit is this?!....")

                time_unit_idx = i
            i += 1

        if for_idx > 0 and time_unit_idx > 0:
            time_amt = word_split[for_idx + 1:time_unit_idx]
        else:
            time_amt = '' 
        recipe_item = {'sentence_id': sentence_id, 'time_amt': time_amt, 'time_unit': time_unit}
        recipe_schedule.append(recipe_item)
        sentence_id += 1

    for instruction in recipe_schedule:
        instruction_text = recipe_instructions[instruction['sentence_id']]
        speech_heard = "y"
        user_speech = "error"

        while (speech_heard.lower() == "y"):
            speak(instruction_text)
            speak("Do you want me to say that again? Please say yes or no.")
            user_speech = recognize_speech_from_mic()

            while user_speech[0] not in ["y", "n"]:
                speak("I didn't catch that. Do you want me to say that again? Please say yes or no.")
                user_speech = recognize_speech_from_mic()
            speech_heard = user_speech[0]
            print(speech_heard)

        if instruction["time_amt"]:
            times = " to ".join(instruction["time_amt"])
            speak("This instruction takes " + times + " " + instruction["time_unit"] + ". Do you want me to set a timer for " + instruction["time_amt"][0] + " " + instruction["time_unit"] + "?")
            user_speech = recognize_speech_from_mic()[0].lower()

            while user_speech[0] not in ["y", "n"]:
                speak("Sorry, I didn't catch that. Do you want me to set a time for " + instruction["time_amt"][0] + " " + instruction["time_unit"] + "? Please say yes or no.")
                user_speech = recognize_speech_from_mic()

            if user_speech == "y":
                speak("Ok, setting a timer...")            
                speak("How many minutes shall i sleep for before I start the timer? You can extend this afterwards if you need more time.")
                user_speech = recognize_speech_from_mic()
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

                if user_speech.isdigit():
                    speak("Sure, I will sleep for " + user_speech + " minutes.")
                else:
                    speak("Sorry, I didn't catch that. I will start the timer in 1 minute.")
                    user_speech = 1
                    
                for i in range(int(user_speech) * 10):
                    print(i)
                    time.sleep(1)
                
        else:
            speak("No timings here. Onto the next instruction")

if __name__ == "__main__":
    main()