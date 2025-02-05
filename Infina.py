import pyttsx3  # For text-to-speech conversion
import speech_recognition as sr  # For speech recognition
import datetime  # For handling time-based operations
import wikipedia  # For Wikipedia search functionality
import webbrowser  # For opening websites in the browser
import os  # For interacting with the operating system (e.g., files)
import requests  # For making HTTP requests (to fetch weather data)
import pyjokes  # For telling random jokes
import psutil  # For system-related information (e.g., CPU, battery)

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')  # Use the sapi5 engine for speech synthesis
voices = engine.getProperty('voices')  # Get available voices
engine.setProperty('voice', voices[0].id)  # Set the voice to the first available voice

def speak(audio):
    """Converts text to speech."""
    engine.say(audio)  # Converts text to speech
    engine.runAndWait()  # Waits for the speech to complete

def wishMe():
    """Greets the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)  # Get current hour
    if hour < 12:
        speak("Good Morning!")  # Greet if before noon
    elif 12 <= hour < 18:
        speak("Good Afternoon!")  # Greet if afternoon
    else:
        speak("Good Evening!")  # Greet if evening
    speak("I am Infina, your AI Assistant. How may I assist you?")  # Introduce the assistant

def takeCommand():
    """Takes microphone input from the user and returns text."""
    recognizer = sr.Recognizer()  # Initialize the speech recognizer
    with sr.Microphone() as source:  # Use the microphone as the audio source
        print("Listening...")  # Inform the user that listening has started
        recognizer.pause_threshold = 1  # Set pause threshold to ignore small pauses
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        print("Recognizing...")  # Inform the user that recognition is in progress
        query = recognizer.recognize_google(audio, language='en-in')  # Recognize speech using Google API
        print(f"User said: {query}\n")  # Print what the user said
    except Exception:
        print("Could not understand, please say that again...")  # Handle unrecognized speech
        return "None"  # Return "None" if the speech was not recognized
    return query.lower()  # Return the recognized speech in lowercase

def getWeather(city="Chennai"):
    """Fetches weather details for a given city using OpenWeather API."""
    api_key = "53f6962bfcfcaf41e42b2a7afd9b8b58"  # Replace with your OpenWeather API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"  # API URL for weather data
    response = requests.get(base_url)  # Make an HTTP GET request to the API
    data = response.json()  # Parse the response into JSON format

    if data["cod"] != "404":  # Check if the city was found in the API response
        temp = data["main"]["temp"]  # Extract temperature
        desc = data["weather"][0]["description"]  # Extract weather description
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")  # Read the weather details aloud
    else:
        speak("City not found. Please check the name.")  # Handle case when city is not found

def tellJoke():
    """Tells a random joke."""
    joke = pyjokes.get_joke()  # Get a random joke using the pyjokes library
    print(joke)  # Print the joke to the console
    speak(joke)  # Read the joke aloud

def systemStatus():
    """Checks and reports CPU and battery status."""
    battery = psutil.sensors_battery()  # Get battery status using psutil
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage percentage
    speak(f"Your system CPU usage is at {cpu_usage} percent. Battery level is at {battery.percent} percent.")  # Read system status aloud

def setReminder(reminder_text):
    """Saves a reminder to a file."""
    with open("reminders.txt", "a") as file:  # Open the reminders file in append mode
        file.write(f"{datetime.datetime.now()} - {reminder_text}\n")  # Write the reminder with timestamp
    speak("Reminder has been set successfully!")  # Confirm the reminder has been set

def readReminders():
    """Reads saved reminders from the file."""
    if os.path.exists("reminders.txt"):  # Check if the reminders file exists
        with open("reminders.txt", "r") as file:  # Open the reminders file in read mode
            reminders = file.readlines()  # Read all lines (reminders)
        if reminders:  # If there are any reminders
            speak("Here are your reminders:")  # Inform the user
            for reminder in reminders[-5:]:  # Read the last 5 reminders
                print(reminder.strip())  # Print each reminder to the console
                speak(reminder)  # Read each reminder aloud
        else:
            speak("You have no reminders.")  # Inform the user if no reminders are saved
    else:
        speak("You have no reminders.")  # Inform the user if the file does not exist

if __name__ == "__main__":
    wishMe()  # Greet the user and introduce the assistant

    while True:
        query = takeCommand()  # Wait for the user to give a command

        # Tell what it can do
        if 'what can you do' in query:
            response = (
                "I can search Wikipedia, open YouTube, Google, and Stack Overflow, "
                "play music, tell the time, check the weather, tell jokes, "
                "report system status, and set reminders. How can I help you today?"
            )
            print(response)  # Print the response to the console
            speak(response)  # Read the response aloud

        # AI Assistant Name
        elif 'your name' in query:
            speak("I am Infina, your AI Assistant.")  # Respond with the assistant's name

        # Wikipedia Search
        elif 'wikipedia' in query:
            speak("Searching Wikipedia...")  # Inform the user that a Wikipedia search is starting
            query = query.replace("wikipedia", "")  # Remove the word "wikipedia" from the query
            results = wikipedia.summary(query, sentences=2)  # Get the top 2 sentences from Wikipedia
            speak("According to Wikipedia")  # Inform the user that the answer is from Wikipedia
            print(results)  # Print the Wikipedia summary
            speak(results)  # Read the Wikipedia summary aloud

        # Open Websites
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")  # Open YouTube in the browser

        elif 'open google' in query:
            webbrowser.open("google.com")  # Open Google in the browser

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")  # Open Stack Overflow in the browser

        # Play Music
        elif 'play music' in query:
            music_dir = 'D:\\songs\\favorite'  # Path to the music directory
            songs = os.listdir(music_dir)  # List all files in the music directory
            os.startfile(os.path.join(music_dir, songs[0]))  # Play the first song in the directory

        # Check Time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  # Get the current time
            speak(f"The time is {strTime}")  # Read the time aloud

        # Get Weather
        elif 'weather' in query:
            speak("Which city would you like to check?")  # Ask the user for the city name
            city = takeCommand()  # Take the city name as input
            if city != "None":
                getWeather(city)  # Fetch and read the weather for the specified city

        # Tell a Joke
        elif 'joke' in query:
            tellJoke()  # Tell a random joke

        # System Status
        elif 'system status' in query:
            systemStatus()  # Report the system's CPU and battery status

        # Set Reminder
        elif 'set reminder' in query:
            speak("What should I remind you about?")  # Ask the user for the reminder text
            reminder_text = takeCommand()  # Take the reminder text as input
            if reminder_text != "None":
                setReminder(reminder_text)  # Save the reminder to the file

        # Read Reminders
        elif 'read reminders' in query:
            readReminders()  # Read the saved reminders aloud

        # Exit
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye! Have a great day!")  # Say goodbye to the user
            break  # Exit the loop and stop the assistant