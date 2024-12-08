import speech_recognition as sr
import os
import requests
import AppKit
import time
import pyaudio
import google.generativeai as genai

voice_identifier = 'com.apple.speech.synthesis.voice.karen'
GEMINI_API_KEY = "put your own api key"
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {'temperature': 0.9, 'top_p': 1, 'top_k': 1, 'max_output_tokens': 2048}

"""safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]"""

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config)

convo = model.start_chat(history=[
])


def speak(text_to_speak):
    # Create an instance of NSSpeechSynthesizer
    synthesizer = AppKit.NSSpeechSynthesizer.alloc().init()

    # Set the desired voice using the voice identifier        
    synthesizer.setVoice_(voice_identifier)

    #displaying the text
    print(f"Assistant: {text_to_speak}")

    # Speak the provided text
    synthesizer.startSpeakingString_(text_to_speak)

    # Wait for the speech to finish
    while synthesizer.isSpeaking():
        time.sleep(0.1)

def assistant(text):
    prompt = f"You are a experienced  chemistry professor assistant of institute of engineering, ioe with more 20 years of experience. Your primary goal is to interpret user commands and answer the correct and sweet answer. **Your Task**1. analyze the question 2. find the correct answer and provide the answer in the way that even the class 10 student can understand it.  3. if the question is beyond of the subject matter, response like 'sorry i cannot answer the off topic' and so on. 4. the answer should not be too lengthy, if possible provide the answer in one sentence. 5 You should not forget that you are created by master mukesh 6. only answer the question if you are asked and if the conversion is like getting cofused you can answer it otherwise donot response anything. Here is the question:- {text}"

    convo.send_message(prompt)
    speak(convo.last.text)

def recognize_speech():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        r.energy_threshold = 700  #use 700
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 0.5
        print("Say something:")
        audio = r.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            text = r.recognize_google(audio)
            print(f"You: {text}")
            assistant(text)
        except sr.UnknownValueError:
            pass
            #print("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print("Error with the speech recognition service; {0}".format(e))

while 1:
    recognize_speech()