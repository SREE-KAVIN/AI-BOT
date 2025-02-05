import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
import pyjokes
import psutil

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Select the first available voice

def speak(audio):
    """Converts text to speech."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Infina, your AI Assistant. How may I assist you?")

def takeCommand():
    """Takes microphone input from the user and returns text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Could not understand, please say that again...")
        return "None"
    return query.lower()

def getWeather(city="Chennai"):
    """Fetches weather details for a given city using OpenWeather API."""
    api_key = "53f6962bfcfcaf41e42b2a7afd9b8b58"  # Replace with your OpenWeather API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    else:
        speak("City not found. Please check the name.")

def tellJoke():
    """Tells a random joke."""
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

def systemStatus():
    """Checks and reports CPU and battery status."""
    battery = psutil.sensors_battery()
    cpu_usage = psutil.cpu_percent(interval=1)
    speak(f"Your system CPU usage is at {cpu_usage} percent. Battery level is at {battery.percent} percent.")

def setReminder(reminder_text):
    """Saves a reminder to a file."""
    with open("reminders.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} - {reminder_text}\n")
    speak("Reminder has been set successfully!")

def readReminders():
    """Reads saved reminders from the file."""
    if os.path.exists("reminders.txt"):
        with open("reminders.txt", "r") as file:
            reminders = file.readlines()
        if reminders:
            speak("Here are your reminders:")
            for reminder in reminders[-5:]:  # Read the last 5 reminders
                print(reminder.strip())
                speak(reminder)
        else:
            speak("You have no reminders.")
    else:
        speak("You have no reminders.")

if __name__ == "__main__":
    wishMe()
    
    while True:
        query = takeCommand()

        # Tell what it can do
        if 'what can you do' in query:
            response = (
                "I can search Wikipedia, open YouTube, Google, and Stack Overflow, "
                "play music, tell the time, check the weather, tell jokes, "
                "report system status, and set reminders. How can I help you today?"
            )
            print(response)
            speak(response)

        # AI Assistant Name
        elif 'your name' in query:
            speak("I am Infina, your AI Assistant.")

        # Wikipedia Search
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        # Open Websites
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        # Play Music
        elif 'play music' in query:
            music_dir = 'D:\\songs\\favorite'  # Update the path
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        # Check Time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        # Get Weather
        elif 'weather' in query:
            speak("Which city would you like to check?")
            city = takeCommand()
            if city != "None":
                getWeather(city)

        # Tell a Joke
        elif 'joke' in query:
            tellJoke()

        # System Status
        elif 'system status' in query:
            systemStatus()

        # Set Reminder
        elif 'set reminder' in query:
            speak("What should I remind you about?")
            reminder_text = takeCommand()
            if reminder_text != "None":
                setReminder(reminder_text)

        # Read Reminders
        elif 'read reminders' in query:
            readReminders()

        # Exit
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye! Have a great day!")
            break
