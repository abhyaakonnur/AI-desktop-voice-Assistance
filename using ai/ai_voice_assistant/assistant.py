import os
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import webbrowser as web
import wikipediaapi
import openai
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

class VoiceAssistant:
    _engine = None  # Class variable to ensure single TTS engine instance
    
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine (only once)
        if VoiceAssistant._engine is None:
            VoiceAssistant._engine = pyttsx3.init()
            self.engine = VoiceAssistant._engine
            self.engine.setProperty('rate', 180)  # Speed of speech
            
            # Set voice (0 for male, 1 for female)
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)  # Female voice
        else:
            self.engine = VoiceAssistant._engine
        
        # Initialize Wikipedia
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='MyVoiceAssistant/1.0 (your@email.com)'
        )
        
        # Assistant's name
        self.name = "Ava"
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError as e:
            if 'run loop already started' in str(e):
                # If the loop is already running, create a new engine instance
                self.engine = pyttsx3.init()
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                raise e
    
    def listen(self):
        """Listen for audio input and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.pause_threshold = 1
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    print("Recognizing...")
                    query = self.recognizer.recognize_google(audio, language='en-in')
                    print(f"You: {query}")
                    return query.lower()
                except sr.WaitTimeoutError:
                    print("Listening timed out. Please try again.")
                    return ""
                except sr.UnknownValueError:
                    print("Sorry, I didn't catch that. Could you please repeat?")
                    return ""
                except sr.RequestError as e:
                    print(f"Could not request results; check your internet connection. Error: {e}")
                    return ""
        except OSError as e:
            print(f"Microphone error: {e}")
            print("Please check if your microphone is properly connected.")
            return ""
    
    def get_ai_response(self, prompt):
        """Get response from OpenAI's API"""
        try:
            if not os.getenv('OPENAI_API_KEY'):
                return "OpenAI API key is not set. Please check your .env file."
                
            from openai import OpenAI
            client = OpenAI()
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                timeout=10  # Add timeout to prevent hanging
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e).lower()
            if "authentication" in error_msg or "invalid api key" in error_msg:
                return "Error: Invalid OpenAI API key. Please check your .env file."
            elif "rate limit" in error_msg or "too many requests" in error_msg:
                return "I'm getting too many requests. Please try again in a moment."
            elif "connection" in error_msg:
                return "I'm having trouble connecting to the AI service. Please check your internet connection."
            else:
                return f"I encountered an error: {str(e)}"
    
    def wish_me(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good morning!")
        elif 12 <= hour < 18:
            self.speak("Good afternoon!")
        else:
            self.speak("Good evening!")
        
        self.speak(f"I am {self.name}, your AI assistant. How can I help you today?")
    
    def _open_website(self, url):
        """Helper method to open a website with improved error handling"""
        try:
            webbrowser.open(url, new=2)
            # Extract and return a clean website name for the response
            clean_url = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
            return f"Opening {clean_url}"
        except Exception as e:
            error_msg = f"Error opening {url}: {str(e)}"
            print(error_msg)
            return "I'm having trouble opening that website. Please try again or check your internet connection."
    
    def _play_on_youtube(self, song):
        """Helper method to play a song on YouTube"""
        try:
            search_url = f'https://www.youtube.com/results?search_query={song.replace(" ", "+")}'
            webbrowser.open(search_url, new=2)  # new=2 opens in a new tab if possible
            return f"Playing {song} on YouTube"
        except Exception as e:
            error_msg = f"Error playing {song} on YouTube: {str(e)}"
            print(error_msg)
            return "I'm having trouble playing that song on YouTube. Please try again or check your internet connection."
    
    def _get_current_time(self):
        """Helper method to get the current time"""
        try:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        except Exception as e:
            error_msg = f"Error getting current time: {str(e)}"
            print(error_msg)
            return "I'm having trouble getting the current time. Please try again."
    
    def _get_current_date(self):
        """Helper method to get the current date"""
        try:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            return f"Today's date is {current_date}"
        except Exception as e:
            error_msg = f"Error getting current date: {str(e)}"
            print(error_msg)
            return "I'm having trouble getting the current date. Please try again."

    def _open_application(self, app_name):
        """Try to open a native application by name on the host OS (Windows)."""
        try:
            import shutil
            import subprocess
            # Try to find executable in PATH first
            exe = shutil.which(app_name)
            if exe:
                subprocess.Popen([exe])
                return f"Opening {app_name}"

            # Common Windows install locations for Firefox
            if app_name.lower() in ['firefox', 'mozilla firefox']:
                possible_paths = [
                    r"C:\Program Files\Mozilla Firefox\firefox.exe",
                    r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
                ]
                for p in possible_paths:
                    if os.path.exists(p):
                        subprocess.Popen([p])
                        return "Opening Firefox"

            # Fallback: if app is whatsapp, open WhatsApp Web in browser
            if 'whatsapp' in app_name.lower():
                return self._open_website('https://web.whatsapp.com')

            # Final fallback: try opening a web search for the app
            search_url = f'https://www.google.com/search?q={app_name.replace(" ", "+")}'
            webbrowser.open(search_url, new=2)
            return f"Opening search for {app_name}"
        except Exception as e:
            print(f"Error opening application {app_name}: {e}")
            return "I couldn't open that application. Please try again."

    def _search_google(self, query):
        """Open a Google search for the given query and return a friendly message."""
        try:
            from urllib.parse import quote_plus
            q = query.strip()
            if not q:
                return "What would you like me to search for on Google?"
            search_url = f'https://www.google.com/search?q={quote_plus(q)}'
            webbrowser.open(search_url, new=2)
            return f"Searching Google for {q}"
        except Exception as e:
            print(f"Error performing Google search: {e}")
            return "I couldn't perform the search. Please try again."
    
    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        try:
            page = self.wiki.page(query)
            if page.exists():
                return page.summary[:500]  # Return first 500 characters
            else:
                return "I couldn't find any information on that topic."
        except Exception as e:
            return "Sorry, I encountered an error while searching Wikipedia."
    
    def process_command(self, command):
        """Process user commands"""
        if 'wikipedia' in command:
            self.speak('Searching Wikipedia...')
            query = command.replace("wikipedia", "")
            result = self.search_wikipedia(query)
            response = "According to Wikipedia, " + result
            self.speak(response)
            return response

        # Handle quick Google searches from voice
        if command.startswith('search ') or 'search for' in command or (command.startswith('google ') and len(command.split())>1):
            # Normalize and extract query
            query = command
            for prefix in ['search for', 'search', 'google']:
                if query.startswith(prefix):
                    query = query[len(prefix):].strip()
                    break
            if not query:
                self.speak("What would you like me to search for on Google?")
                return ""
            response = self._search_google(query)
            self.speak(response)
            return response
        
        elif 'open youtube' in command:
            self.speak("Opening YouTube.")
            return self._open_website("https://www.youtube.com")
        
        elif 'open google' in command:
            self.speak("Opening Google.")
            return self._open_website("https://www.google.com")
        
        elif 'play' in command:
            song = command.replace('play', '').strip()
            response = f'Playing {song} on YouTube'
            self.speak(response)
            return self._play_on_youtube(song)
        
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            self.speak(response)
            return response
        
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            response = f"Today's date is {current_date}"
            self.speak(response)
            return response
        
        elif 'exit' in command or 'goodbye' in command or 'bye' in command:
            response = "Goodbye! Have a great day!"
            self.speak(response)
            return response
        
        else:
            # For any other query, use OpenAI's API
            response = self.get_ai_response(command)
            self.speak(response)
            return response
    
    def process_web_command(self, command):
        """Process commands for the web interface with improved error handling"""
        try:
            if not command or not command.strip():
                return "I didn't catch that. Could you please repeat?"
                
            command = command.lower().strip()
            
            # Handle web-specific commands
            if 'open youtube' in command:
                return self._open_website("https://www.youtube.com")
            elif 'open google' in command:
                return self._open_website("https://www.google.com")
            # Handle web search commands
            elif command.startswith('search ') or 'search for' in command or (command.startswith('google ') and len(command.split())>1):
                query = command
                for prefix in ['search for', 'search', 'google']:
                    if query.startswith(prefix):
                        query = query[len(prefix):].strip()
                        break
                if not query:
                    return "What would you like me to search for on Google?"
                return self._search_google(query)
            elif command.startswith('open '):
                # Try to open applications or websites
                app = command.replace('open', '', 1).strip()
                # If it's a clear website keyword
                if 'youtube' in app:
                    return self._open_website('https://www.youtube.com')
                if 'google' in app:
                    return self._open_website('https://www.google.com')
                if 'whatsapp' in app:
                    return self._open_website('https://web.whatsapp.com')
                # Try opening a native application (Windows)
                return self._open_application(app)
            elif 'play' in command and 'youtube' not in command:
                song = command.replace('play', '').strip()
                return self._play_on_youtube(song)
            elif 'time' in command:
                return self._get_current_time()
            elif 'date' in command:
                return self._get_current_date()
            elif 'wikipedia' in command:
                query = command.replace('wikipedia', '').strip()
                if not query:
                    return "What would you like me to look up on Wikipedia?"
                return self.search_wikipedia(query)
            else:
                # For all other queries, use AI response
                return self.get_ai_response(command)
                
        except Exception as e:
            error_msg = f"Error in process_web_command: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return "I'm sorry, I encountered an error processing your request. Please try again."

def main():
    assistant = VoiceAssistant()
    assistant.wish_me()
    
    running = True
    while running:
        query = assistant.listen()
        if query:
            running = assistant.process_command(query)

if __name__ == "__main__":
    main()
