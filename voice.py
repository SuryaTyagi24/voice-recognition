import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random

# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

print("\033[4m\033[1m" + "\t\t\t\t\t\t\tJARVISH VOICE ASSISTANCE" + "\033[0m")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Namastay , Mam!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon , Mam!")
    else:
        speak("Good Evening , Mam!")
    speak("I am JARVISH. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("No speech detected in the last 5 seconds. Stopping listening.")
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        speak("Could not request results; check your network connection.")
        return "None"
    return query

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your-email@gmail.com', 'your-password')
        server.sendmail('your-email@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email")

def tell_joke():
    jokes = [
        "Why did the golgappa go to school? Because it wanted to become a 'paani puri'-st!",
        "Why was the computer cold? It left its Windows open!",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why don't we tell secrets on a farm? Because the potatoes have eyes, the corn has ears, and the beans stalk!",
        "Why was the math book sad? Because it had too many problems!",
        "Why did the mobile phone go to school? To improve its 'cell-f' esteem!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ]
    joke = random.choice(jokes)
    return joke

def manage_notes_and_tasks():
    notes = []
    while True:
        speak("What would you like to do with your notes and tasks?")
        action = takeCommand().lower()

        if "add" in action:
            speak("What would you like to add?")
            note = takeCommand()
            notes.append(note)
            speak("Note added.")
        elif "read" in action:
            if not notes:
                speak("You have no notes or tasks.")
            else:
                speak("Here are your notes and tasks:")
                for i, note in enumerate(notes, 1):
                    speak(f"Note {i}: {note}")
        elif "update" in action:
            if not notes:
                speak("You have no notes or tasks to update.")
            else:
                try:
                    speak("Which note or task would you like to update? Please specify the number.")
                    index = int(takeCommand())
                    if 1 <= index <= len(notes):
                        original_note = notes[index - 1]
                        speak(f"You selected note {index}: {original_note}. What would you like to update it to?")
                        new_note = takeCommand()
                        if new_note:
                            notes[index - 1] = new_note
                            speak("Note updated successfully.")
                        else:
                            speak("No new content provided. Note remains unchanged.")
                    else:
                        speak("Invalid note number.")
                except ValueError:
                    speak("Invalid input. Please specify a valid note number.")
        elif "delete" in action:
            if not notes:
                speak("You have no notes or tasks to delete.")
            else:
                speak("Which note or task would you like to delete? Please specify the number.")
                try:
                    index = int(takeCommand())
                    if 1 <= index <= len(notes):
                        deleted_note = notes.pop(index - 1)
                        speak(f"Note deleted: {deleted_note}")
                    else:
                        speak("Invalid note number.")
                except ValueError:
                    speak("Invalid input. Please specify a valid note number.")
        elif "exit" in action:
            speak("Exiting the notes and tasks feature.")
            break
        else:
            speak("Sorry, I didn't understand your request. Please try again.")

def length_conversion(value, from_unit, to_unit):
    conversions = {
        "meters": {"meters": 1, "feet": 3.28084, "inches": 39.3701},
        "feet": {"meters": 0.3048, "feet": 1, "inches": 12},
        "inches": {"meters": 0.0254, "feet": 0.0833333, "inches": 1}
    }
    try:
        result = value * conversions[from_unit][to_unit]
        return result
    except KeyError:
        return None

def weight_conversion(value, from_unit, to_unit):
    conversions = {
        "kilograms": {"kilograms": 1, "pounds": 2.20462},
        "pounds": {"kilograms": 0.453592, "pounds": 1}
    }
    try:
        result = value * conversions[from_unit][to_unit]
        return result
    except KeyError:
        return None

wishMe()

while True:
    query = takeCommand().lower()

    if 'in wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
        speak("Thank you")

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        webbrowser.open("google.com")

    elif 'play music' in query:
        music_dir = music_dir =  r'C:\Users\tyagi\Downloads'

        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            speak("No songs found in the directory.")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'send an email' in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            speak("Please enter the email to whom you want to send your message.")
            to = input("E-mail: ")
            sendEmail(to, content)
        except Exception as e:
            print(e)
            speak("Sorry, I am not able to send this email")

    elif 'calculation' in query:
        speak("Sure, please provide the mathematical expression.")
        expression = input("Expression: ")
        try:
            result = eval(expression)
            print(f"Result: {result}")
            speak(f"The result of {expression} is {result}")
        except Exception as e:
            speak("Sorry, I couldn't calculate that.")

    elif 'joke' in query:
        speak("Sure, here I present you a funny one.")
        speak(tell_joke())
        speak("Hope you enjoyed it")

    elif 'note' in query:
        manage_notes_and_tasks()

    elif 'conversion' in query:
        speak("Sure, I can help you with unit conversion. Please specify the value.")
        value = float(takeCommand())

        speak("Great! Now, please tell me the source unit (e.g., meters, feet, kilograms, pounds).")
        from_unit = takeCommand().lower()

        speak("Excellent! Now, tell me the target unit (e.g., meters, feet, kilograms, pounds).")
        to_unit = takeCommand().lower()

        result = None

        if from_unit in ["meters", "feet", "inches"] and to_unit in ["meters", "feet", "inches"]:
            result = length_conversion(value, from_unit, to_unit)
        elif from_unit in ["kilograms", "pounds"] and to_unit in ["kilograms", "pounds"]:
            result = weight_conversion(value, from_unit, to_unit)

        if result is not None:
            speak(f"{value} {from_unit} is equal to {result:.2f} {to_unit}.")
        else:
            speak("I'm sorry, I can't perform this unit conversion.")

    elif 'exit' in query:
        speak("Bye. See you later.")
        break

    else:
        speak("Sorry, no query matched from my database. Please speak again or try with different commands.")
        print("No query matched")
