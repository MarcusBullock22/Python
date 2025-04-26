import openai
import pyttsx3
import speech_recognition as sr
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


openai.api_key = ""  # Replace with your OpenAI GPT-3/4 API key

# Initialize pyttsx3 engine for TTS (Text to Speech)
engine = pyttsx3.init()

# Initialize Speech Recognition
recognizer = sr.Recognizer()

# Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Set the pad_token_id to eos_token_id
tokenizer.pad_token = tokenizer.eos_token

# Function to generate GPT-3/4 response
def generate_gpt_response(query):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or use "gpt-3.5-turbo" or "gpt-4" depending on your API access
        prompt=query,
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Speech-to-Text using Google Web Speech API
def listen_google():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for input
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return ""

# Text-to-Speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()  # Block while speaking

# Function to listen, process the command, and speak the response
def listen_and_respond():
    command = listen_google()  

    if command:
        # Generate GPT-3/4 response for any query
        response = generate_gpt_response(command)  # Process with GPT-3/4
        print("Jarvis says:", response)
        speak(response)  # Speak the GPT-3/4 response

# Main function to run Jarvis
def run_jarvis():
    while True:
        listen_and_respond()  # Continuously listen and respond to voice commands

# Run Jarvis
run_jarvis()
