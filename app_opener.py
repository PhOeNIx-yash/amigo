import pyautogui
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

def open_windows_app(app_name):
    """
    Opens a Windows application using the Start menu search.
    
    Args:
        app_name (str): The name of the application to open
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Press Windows key to open Start menu
        pyautogui.press('win')
        pyautogui.sleep(1)  # Wait for Start menu to open
        
        # Type the app name
        pyautogui.write(app_name)
        pyautogui.sleep(1)  # Wait for search results
        
        # Press Enter to open the app
        pyautogui.press('enter')
        speak(f"Opening {app_name}")
        return True
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}")
        print(f"Error opening app: {e}")
        return False 