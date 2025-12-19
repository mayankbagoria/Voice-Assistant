# 🎙️ Voice Assistant using Python

A smart voice assistant built with **Python**. It performs tasks such as searching the web, playing music, fetching news updates, checking weather info, and answering general queries using AI.

[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)

---

## 🚀 Features

- 👂 **Wake Word Detection**: Activates on "hello" keyword
- 🎧 **Voice interaction** using `speech_recognition` and `sounddevice`
- 🌐 **Smart web search** via Google Custom Search API
- 🎵 **Music playback** from YouTube Music
- 📰 **Latest news headlines** using NewsAPI
- 🌦️ **Weather and AQI reports**
- 🤖 **AI-based responses** using Google Gemini
- 🗣️ **Text-to-speech responses**

---
## 📦 Requirements

1. [![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
2. Modules in the `requirements.txt`
3. **API** keys

---
## 🛠️How to Run locally

1. 📥 **Clone Or Download** (place all files in a single folder)
2. 🔑 Place **API keys** in the `.env.example` file. (Link to APIs given below) 
3. 🖱️ Rename `.env.example` into `.env` (i.e. Remove `.example` from the file name )
4. ⚙️ Install Required modules :
`pip install -r requirements.txt`
5. ▶️ **Run the Assistant :**
`python main.py`
6. 🗣 Speak the activation word (`hello`), followed by your command.

---
## 📱 Demo Commands

- “**open YouTube**” — Opens YouTube in your browser  
- “**play Shape of You**” — Plays the song on YouTube Music  
- “**what’s the news**” — Reads top 5 current headlines  
- “**weather in Delhi**” — Speaks weather and air quality  
- “**tell me a joke**” — AI-generated response  

---
## 🔑 API Keys Required

You’ll need to obtain API keys(Free) from various services:

| Service | Description | Link |
|----------|--------------|------------------|
| Google Custom Search API | Used for web search | [`Get your Search API`](https://developers.google.com/custom-search/v1/introduction/) |
| Google Programmable Search Engine ID | Custom search engine ID | [`Get your ID`](https://programmablesearchengine.google.com/controlpanel/all) |
| NewsAPI | For the latest news | [`Get your News API`](https://newsapi.org/) |
| Google Gemini | AI response generation | [`Get your Gemini API`](https://aistudio.google.com/apikey) |
| OpenWeather & AQI API | For weather and air quality | [`Get your Weather API`](https://www.weatherapi.com/) [`Get your AQI API`](https://aqicn.org/data-platform/token/) |

⚠️**NOTE :** During getting google search engine id in 'what to search' section select 'Entire web'

---

## 🔧 Custom Module

**`weather.py`** handles OpenWeatherMap + AQI API integration:
```python
def weatherf(city, weather_key, aqi_key):
    # Returns (speech_text,weather_report, aqi_report)
    pass
```

---
## 🧠 AI Configuration

The AI function uses **Gemini 2.5 Flash** model for quick, relevant responses

---

## 🏗️ Code Architecture

Main components of the script:

- **`Config:`** .env → API Keys
- **`speak(data)`** – Converts text to speech  
- **`getMusicURL(query)`** – Fetches best match from YouTube Music  
- **`getSiteURL(site)`** – Uses Google Custom Search for web results  
- **`music(song)` / `web(site)`** – Opens music or websites in browser  
- **`news()`** – Fetches top headlines  
- **`weather(city)`** – Retrieves weather and AQI data  
- **`AIprocess(prompt)`** – Uses Gemini API for intelligent answers  
- **`process_cmd(cmd)`** – Handles user command detection  
- **`main()`** – Continuously listens and executes actions  
---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "No command detected" | Check microphone permissions |
| API errors | Verify `.env` keys, internet connection |

---
**Author**: Mayank Bagoria  
**Language**: Python 3.12+  
**Version**: 1.0

---

