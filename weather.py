import requests
import json
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_weather(city):
    api_key = "USE OPEN WEATHER MAP API"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # This will give temperature in Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            main = data["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            pressure = main["pressure"]
            weather_desc = data["weather"][0]["description"]
            
            weather_info = f"The weather in {city} is {weather_desc}. "
            weather_info += f"The temperature is {temperature}°C. "
            weather_info += f"Humidity is {humidity}% and pressure is {pressure} hPa."
            
            return weather_info
        else:
            return f"Error: {data.get('message', 'Unknown error')}"
            
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

def weather_command(query):
    # Extract city name from the query
    if "weather in" in query:
        city = query.split("weather in")[1].strip()
    elif "weather of" in query:
        city = query.split("weather of")[1].strip()
    else:
        city = query.split("weather")[1].strip()
    
    weather_info = get_weather(city)
    print(weather_info)
    
    speak(weather_info)
    
    return weather_info 
