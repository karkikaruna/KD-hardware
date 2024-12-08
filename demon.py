import speech_recognition as sr
import time
import pyttsx3  # Text-to-speech for Windows
import google.generativeai as genai

# Configuration for Google Generative AI
GEMINI_API_KEY = "put your own api key"  # Replace with your Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    'temperature': 0.9,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)
convo = model.start_chat(history=[])

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking speed (words per minute)
engine.setProperty('volume', 1.0)  # Set volume (1.0 is maximum)

# Voice selection (ensure the desired voice is available on your system)
voices = engine.getProperty('voices')
# Select a female voice (adjust index if needed)
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

def speak(text_to_speak):
    """Speak the provided text using pyttsx3."""
    print(f"Assistant: {text_to_speak}")  # Display text on the console
    engine.say(text_to_speak)
    engine.runAndWait()  # Wait for the speech to finish

def assistant(text):
    """Handle user input and generate a response."""
    prompt = (
        f"You are an experienced chemistry professor assistant of the Institute of Engineering (IOE) with more than 20 years of experience. "
        f"Your primary goal is to interpret user commands and provide the correct and concise answer in a way that even a class 10 student can understand. "
        f"If the question is beyond your subject area, respond with something like 'Sorry, I cannot answer the off-topic question.' "
        f"Here is the question: {text}"
    )

    convo.send_message(prompt)
    speak(convo.last.text)

def recognize_speech():
    """Capture and recognize speech input."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.energy_threshold = 700  # Set energy threshold
        recognizer.dynamic_energy_threshold = True
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 0.5
        print("Say something:")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            if text.lower() in ["exit", "quit", "stop"]:
                print("Exiting program. Goodbye!")
                exit(0)
            assistant(text)
        except sr.UnknownValueError:
            print("I couldn't catch that. Please try again.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")

# Continuous listening loop
while True:
    recognize_speech()
