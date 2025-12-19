import os
import requests
import time
import threading
import webbrowser
import sounddevice as sd
import speech_recognition as sr
import pyttsx3
from ytmusicapi import YTMusic
from google import genai
from google.genai import types
from dotenv import load_dotenv

from weather import weatherf

WAKE_WORD = "hello"
SAMPLE_RATE = 16000

GOOGLE_SEARCH_API_KEY=GOOGLE_SEARCH_ENGINE_ID=NEWS_API_KEY=GEMINI_API_KEY=WEATHER_API_KEY=AQI_API_KEY=None

load_dotenv()
def config():
    global GOOGLE_SEARCH_API_KEY,GOOGLE_SEARCH_ENGINE_ID,NEWS_API_KEY,GEMINI_API_KEY,WEATHER_API_KEY,AQI_API_KEY,WAKE_WORD
    GOOGLE_SEARCH_API_KEY = os.getenv('GOOGLE_SEARCH_API_KEY')
    GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    AQI_API_KEY = os.getenv('AQI_API_KEY')

    missing = []
    if not GOOGLE_SEARCH_API_KEY: missing.append("GOOGLE_SEARCH_API_KEY")
    if not GOOGLE_SEARCH_ENGINE_ID: missing.append("GOOGLE_SEARCH_ENGINE_ID")
    if not NEWS_API_KEY: missing.append("NEWS_API_KEY")
    if not GEMINI_API_KEY: missing.append("GEMINI_API_KEY")
    if not WEATHER_API_KEY: missing.append("WEATHER_API_KEY")
    if not AQI_API_KEY: missing.append("AQI_API_KEY")

    if missing:
        print(f"Missing API keys in .env: {', '.join(missing)}")
        return False
    return True

recognizer = sr.Recognizer()
ytmusic = YTMusic()

class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.thread = None
    
    def _animate(self):
        if self.is_running:
            print("\x1b[2K",end="")
            print("Listening",end="")
            while self.is_running:
                print(".",end="")
                time.sleep(0.4)
                print(".",end="")
                time.sleep(0.4)
                print(".",end="",flush=True)
                time.sleep(0.4)
                print("\x1b[3D   \b\b\b", end="", flush=True)
                time.sleep(0.4)
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._animate,daemon=True)
            self.thread.start()
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            if self.thread:
                self.thread.join(timeout=1.0)
            print("\x1b[2K\r",end="",flush=True)

def recording(duration):
    audio = sd.rec(int(duration * SAMPLE_RATE),samplerate=SAMPLE_RATE,channels=1,dtype='int16')
    sd.wait()
    audio_bytes = audio.tobytes()
    audio_data = sr.AudioData(audio_bytes, SAMPLE_RATE, 2)
    return audio_data

def speak(data):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(data)
    engine.runAndWait()
    engine = None

def getMusicURL(query):
    results = ytmusic.search(query, filter='songs', limit=1)

    if results:
        track = results[0]

        title = track.get('title', 'Unknown Title')
        video_id = track.get('videoId', '')
        artists = track.get('artists', [])
        if artists:
            artist_names = ', '.join([artist.get('name', '') for artist in artists])
        else:
            artist_names = 'Unknown Artist'
        album = track.get('album', {})
        if album:
            album_name = album.get('name', 'Unknown Album')
        else:
            album_name = 'Unknown Album'
        duration = track.get('duration', 'Unknown')
        youtube_music_url = f"https://music.youtube.com/watch?v={video_id}"

        print("Best Match Found:")
        print(f"Title: {title}")
        print(f"Artist(s): {artist_names}")
        print(f"Album: {album_name}")
        print(f"Duration: {duration}")
        return youtube_music_url
    else:
        print(f"No results found for '{query}'")
        return None

def getSiteURL(site):
    search_url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'key': GOOGLE_SEARCH_API_KEY,
        'cx': GOOGLE_SEARCH_ENGINE_ID,
        'q': site,
        'num': 1
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            url = data['items'][0]['link']
            return url
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def web(cmd):
    url = getSiteURL(cmd)
    webbrowser.open(f"{url}") if url is not None else print("web error")
    print(f"Opening {cmd}")

def music(cmd):
    murl = getMusicURL(cmd)
    webbrowser.open(f"{murl}") if murl is not None else print("web error")
    print(f"Playing {cmd}")

def news():
    query_params = {
      "language": "en",
      "apiKey": NEWS_API_KEY
    }
    main_url = "https://newsapi.org/v2/top-headlines"

    try:
        res = requests.get(main_url, params=query_params)
        res.raise_for_status()
        open_page = res.json()
        articles = open_page["articles"][:5]
        
        for i, ar in enumerate(articles, 1):
            print(f"{i}. {ar['title']}")
            speak(f"News {i}: {ar['title']}")
    except Exception as e:
        speak("News unavailable")
        print(f"News API error: {e}")

def weather(city):

    weather_r,report,aqi_rep = weatherf(city,WEATHER_API_KEY,AQI_API_KEY)
    speak(weather_r)
    print(report)
    print(aqi_rep)

def AIprocess(prompt):
    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        print("prossesing your promt using google's genai")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
            system_instruction="You are a virtual assistant skilled in general tasks like Alexa and Google Cloud. Give short responses please."),
            contents=prompt,
        )
        return response.text
    except:
        print("API Error")
        print("The model is overloaded. Please try again later.")
        return None

def process_cmd(cmd):
    c = list(cmd.split(" "))
    if "open" in c:
        c.remove("open")
        web(' '.join(c))
    elif ("play") in c:
        c.remove("play")
        music(' '.join(c))
    elif "news" in c:
        news()
    elif "weather" in c:
        weather(c[-1])
    else:
        response = AIprocess(cmd)
        speak(response)
    print("Task Done",flush=True)

def main():
    print("Integrating APIs...")
    if not config():
        return
    print("APIs Inegration Successfull")
    loader = LoadingAnimation()
    print("Activating ASSISTANT....",flush=True)
    while True:
        loader.start()
        audio = recording(1.5)
        loader.stop()
        try:
            text = recognizer.recognize_google(audio, language="en-IN").lower()
            r = list(text.split(" "))
            print("You said:", text ,flush=True)
            if WAKE_WORD in r:
                speak("yes sir how can i help you")
                loader.start()
                audio = recording(5)
                loader.stop()
                try:
                    cmd = recognizer.recognize_google(audio, language="en-IN").lower()
                    print("You said:", cmd ,flush=True)
                    process_cmd(cmd)
                except sr.UnknownValueError:
                    print("No command detected")
                except sr.RequestError as e:
                    print(f"API timeout/delay error: {e}")
                    print("⚠️ No internet connection \nThis program requires internet connection to run")
                    break
            elif "exit" in text:
                speak("Goodbye")
                break
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"API timeout/delay error: {e}")
            print("⚠️ No internet connection \nThis program requires internet connection to run")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")