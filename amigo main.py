import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import pyautogui
import datetime
import random
import time
from app_opener import open_windows_app
from weather import weather_command
from plyer import notification
from ai import get_ai_response

# init pyttsx
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

engine.setProperty('voice', voices[0].id)  # 1 for female and 0 for male voice

# Get current speech rate and adjust it
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)  # Decrease the rate to make it slower

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def setup_microphone():
    
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3000  # Adjust based on your microphone
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8  # Longer pause threshold for more natural speech
    recognizer.phrase_threshold = 0.3  # Lower phrase threshold for better phrase detection
    return recognizer

def take_command(max_retries=3):
    
    recognizer = setup_microphone()
    
    for attempt in range(max_retries):
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                
                print("Recognizing...")
                query = recognizer.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                return query.lower()
                
        except Exception as e:
            print(f"Error: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(1)
                continue
            return "None"
    
    return "None"

def respond_to_trigger():
    
    print("Waiting for wake word...")
    while True:
        result = take_command()
        if result == "None":
            continue
        
        # More flexible wake word detection
        wake_phrases = ['hey amigo', 'hi amigo', 'hello amigo', 'amigo']
        if any(phrase in result for phrase in wake_phrases):
            speak("Yes, how can I assist you?")
            return True
        elif 'exit' in result:
            speak("Goodbye!")
            exit(0)

if __name__ == '__main__':
    speak("Amigo assistant activated.")
    speak("Say 'Hey Amigo' to start.")

    while True:
        if respond_to_trigger():
            while True:
                query = take_command()
                if query == "None":
                    print("No command received, waiting for wake word...")
                    break
                    
                # Rest of the command processing remains the same
                if 'wikipedia' in query:
                    speak("Searching Wikipedia ...")
                    query = query.replace("wikipedia", '')
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia")
                    print(results)
                    speak(results)
                
                # Handle conversation using the enhanced model
                elif "google" in query:
                    from Searchnow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from Searchnow import searchYoutube
                    searchYoutube(query)
                    
                # basic tab openings           
                elif 'open chatgpt' in query or 'open chat gpt' in query:
                    speak("opening chat gpt")
                    webbrowser.open("chatgpt.com")
                elif 'open github' in query:
                    speak("opening github")
                    webbrowser.open("github.com")
                elif 'open stackoverflow' in query or "open stack overflow" in query:
                    speak("opening stackoverflow")
                    webbrowser.open("stackoverflow.com")
                elif 'open spotify' in query:
                    speak("opening spotify")
                    webbrowser.open("spotify.com")
      
                # Playing music on youtube        
                elif 'play music' in query:
                    song = query.replace('play music', '').strip()
                    if song:
                        speak(f"Playing {song} on YouTube")
                        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
                    else:
                        speak("What song would you like to hear?")

                # playing fav songs         
                elif "tired" in query or "play my favourite songs" in query or "my playlist" in query:
                    speak("Playing your favourite songs, Boss")
                    a = (1,2,3) 
                    b = random.choice(a)
                    if b==1:
                        webbrowser.open("https://www.youtube.com/watch?v=yUu26tcUri0")                  
                    elif b==2:
                        webbrowser.open("https://www.youtube.com/watch?v=Lo3lxS-6joY")
                    else:
                        webbrowser.open("https://www.youtube.com/watch?v=syFZfO_wfMQ")

                # Screenshot and Photos        
                elif "screenshot" in query:
                    import pyautogui
                    im = pyautogui.screenshot()
                    im.save("ss.jpg")

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")

                # Pause/Play on YouTube or media players
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("Video paused")
                # Resume playing
                elif "play" in query:
                    pyautogui.press("k")  
                    speak("Video played")
                # Mute/Unmute
                elif "mute" in query:
                    pyautogui.press("m")  
                    speak("Video muted")
                # Volume up using keyboard module
                elif "volume up" in query:
                    speak("Turning volume up, boss")
                    pyautogui.press("up") 
                # Volume down using keyboard module        
                elif "volume down" in query:
                    speak("Turning volume down, boss")
                    pyautogui.press("down") 
        
                # Acessing local storage of computer        
                elif 'local disk d' in query:
                    speak("opening local disk D")
                    webbrowser.open("D://")
                elif 'local disk c' in query:
                    speak("opening local disk C")
                    webbrowser.open("C://")
                elif 'local disk e' in query:
                    speak("opening local disk E")
                    webbrowser.open("E://")
                
                # current time        
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"sir, the time is {strTime}")  

                # AI conversation with memory
                elif "chat" in query or "talk to me" in query or "amigo tell me" in query:
                    speak("What would you like to chat about?")
                    chat_query = take_command()
                    if chat_query != "None":
                        response = get_ai_response(chat_query)
                        speak(response)
                        print(f"Amigo AI: {response}")
                
                # Get AI response for any query
                elif "ask ai" in query:
                    ai_query = query.replace("ask ai", "").strip()
                    if ai_query:
                        response = get_ai_response(ai_query)
                        speak(response)
                        print(f"Amigo AI: {response}")
                    else:
                        speak("What would you like to ask the AI?")
                        ai_query = take_command()
                        if ai_query != "None":
                            response = get_ai_response(ai_query)
                            speak(response)
                            print(f"Amigo AI: {response}")
                
                # View conversation history
                elif "conversation history" in query or "chat history" in query:
                    from ai import load_memory
                    memory = load_memory()
                    if memory["conversations"]:
                        speak("Here are your recent conversations:")
                        for i, conv in enumerate(memory["conversations"][-5:], 1):
                            print(f"{i}. You: {conv['user']}")
                            print(f"   Amigo: {conv['assistant']}")
                            # Only speak the most recent conversation
                            if i == len(memory["conversations"][-5:]):
                                speak(f"Your last question was: {conv['user']}")
                                speak(f"And I answered: {conv['assistant']}")
                    else:
                        speak("You don't have any conversation history yet.")
                
                # Clear conversation history
                elif "clear memory" in query or "clear history" in query or "forget our conversations" in query:
                    from ai import save_memory
                    save_memory({"conversations": []})
                    speak("I've cleared our conversation history.")
                
                # remember things
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("amigo","")
                    speak("You told me to remember that"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to remember that" + remember.read())
                    with open("Remember.txt", "r") as file:
                        tasks = file.read()
                    notification.notify(
                        title="Amigo Reminder",
                        message=tasks,
                        app_icon=None,  # Path to an .ico file
                        timeout=5,  # Duration
                    )
                
                    
                # Weather information
                elif "weather" in query:
                    weather_command(query)
                    
                # Calculate numbers    
                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("Amigo","")
                    Calc(query)
                    
                # sleep or exit the code      
                elif "goodbye" in query or "good night" in query or "sleep" in query or "good bye" in query:
                    speak("Say yonaraa boss , Going to sleep")
                    exit()
                    
                # Shutdown
                elif 'shutdown' in query:
                    speak("Are you sure you want to shutdown? Say yes or no.")
                    confirm = take_command()
                    if 'yes' in confirm:
                        os.system("shutdown /s /t 1")
                    else:
                        speak("Shutdown cancelled.")
                        break
               
                # opening apps
                elif "open" in query:
                    # Extract the app name from the query
                    app_name = query.replace("open", "").strip()
                    if app_name:
                        open_windows_app(app_name)
                    else:
                        speak("Please specify which app you want to open")
                
                # If no specific command matches, try AI response as fallback
                else:
                    response = get_ai_response(query)
                    speak(response)
                    print(f"Amigo AI: {response}")
