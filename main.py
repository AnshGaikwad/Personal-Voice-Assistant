from __future__ import print_function
import datetime
import pickle
import os.path
import webbrowser
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pyttsx3
import time
import playsound
import speech_recognition as sr
from gtts import gTTS  # gtts stands for google text to speech
import subprocess  # This will allow us to run processes (like notepad.exe) concurrently with our python script.
import wikipedia
import smtplib
import random

# Every month/day is ordered
MONTHS = ["january", "february", "march", "april", "may", "june"
                                                          "", "july", "august", "september", "october", "november",
          "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# This function will create an audio file (.mp3) that has the google voice saying whatever text we pass in
# It will then save that file to the same directroy as our python script, load it in using playsound and play the sound
def speako(text):
    tts = gTTS(text=text, lang='en')  # This will transform this text into an english audio file
    filename = 'voice.mp3'  # Voice file name and .mp3 extension
    tts.save(filename)  # Saves file
    playsound.playsound(filename)  # Play the mp3 file


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[1].id)  # Set index for voices currently 3 voices available
    engine.say(text)
    engine.runAndWait()


# By a long pause in your speaking it understands it by stop recording
# This function will be able to detect a users voice, translate the audio to text and return it to us
# It will even wait until the user is speaking to start translating/recording the audio
def get_audio():
    r = sr.Recognizer()  # Creating a recognizer object from Speech Recognizer module
    with sr.Microphone() as source:  # Using microphone to get input
        audio = r.listen(source)
        said = ""
        r.pause_threshold = 1  # Press control and study if intrested

        try:
            said = r.recognize_google(audio)  # Converting audio to text
            print(said)
        except Exception as e:  # If it does'nt undersand it gives error rather than crashing
            print("Exception: " + str(e))

    return said.lower()


# The authenticate_google function will be responsible for performing the authentication at the beginning of our script
# The next times you run the program you will not need to perform this step.
# This is because the script we've copied saves our credential information in a .pickle file.
# You can see the file in your main script.
# If you want to change to a new google calendar account simply delete the .pickle file and run the program again.

# LINK of google calender api: https://developers.google.com/calendar/quickstart/python

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


# While the get_events function will get the n amount of events that appear next in our calendar
def get_eventso(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def get_events(day, service):
    # Call the Calendar API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("+")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)


# This function will parse the text passed in and look for a month and/or a day
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:  # if we see today then return today
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():  # Here we start looping through it to find certain keywords
        if word in MONTHS:  # Check index in months
            month = MONTHS.index(word) + 1
        elif word in DAYS:  # Check index in days
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:  # Now we check if any word has day_extensions
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    # CASES:
    # 1. We have a day but no month
    # 2. We have only a day of the week
    # 3. The date mentioned is before the current date
    # 4. We don't find a date

    # If index of month is less than current month obviously user wants information about next year
    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year + 1

    # If index of day is less than current day obviously user wants information about next month
    # This is slighlty different from the video but the correct version
    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()  # Tells us which day of the week it is (it ranges from 0 - 6)
        dif = day_of_week - current_day_of_week

        # Try looking up the calender to understand this algorithm
        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  # FIXED FROM VIDEO
        return datetime.date(month=month, day=day, year=year)


# The first step to create a note is to make a function called note()
# This function will take some text and create and open a note that contains that text
# This function will now save a file with a name as the current date
# Then open that saved file and show it to the user
def note(text):
    date = datetime.datetime.now()  # It will give the current date and time and then we will name our note that, so that the notes will not get overwritten
    file_name = str(date).replace(":", "-") + "-note.txt"  # We will replace : with - as notepad cant have : in it
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("My name is Sofia. Please tell me how may I help you")


def sendEmail(to, content):
    # To use this function you should enable less secure apps in your gmail or this will not work
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


WAKE = "sofia"
wishMe()
SERVICE = authenticate_google()

while True:
    print("Listening")
    text = get_audio()

    if text == WAKE:
        speak("How can I help you {{your-name}}")
        text = get_audio()

        # We want to access get events only when user says the below lines
        # Now that we have everything functioning it's time to determine how/when to use the function get_events().
        # It only makes sense to call it if what we are asking the assistant relates to our calendar.
        # What we are going to do is create a list of phrases that when detected will trigger the call to get_events().

        CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
        for phrase in CALENDAR_STRS:
            if phrase in text:
                date = get_date(text)
                if date:
                    get_events(date, SERVICE)
                else:
                    speak("I don't understand")

        NOTE_STRS = ["make a note", "write this down", "remember this"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to write down?")
                note_text = get_audio()
                note(note_text)
                speak("I've made a note of that.")

        # Logic for executing tasks based on query
        if 'wikipedia' in text:
            speak('Searching Wikipedia...')
            text = text.replace("wikipedia", "")
            results = wikipedia.summary(text, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'youtube' in text:
            webbrowser.open("youtube.com")

        elif 'google' in text:
            webbrowser.open("google.com")

        elif 'stackoverflow' in text:
            webbrowser.open("stackoverflow.com")

        elif 'music' in text:
            music_dir = 'F:\\YOUR_PATH_TO_THE_SONGS_FOLDER\\audios'
            songs = os.listdir(music_dir)
            # print(songs)
            r = random.randint(0, len(songs))
            os.startfile(os.path.join(music_dir, songs[r]))

        elif 'time' in text:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'game' in text:
            codePath = "E:\\YOUR_PATH_TO_A_GAME\\CUBE ESCAPE\\CUBE ESCAPE"
            os.startfile(codePath)

        elif 'email to {{name}}' in text:
            try:
                speak("What should I say?")
                content = get_audio()
                to = "youremail@gmail.com"  # for more cases we can create a dictionary also consisting all the emails
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend {{name}}. I am not able to send this email")
