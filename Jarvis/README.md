# Jarvis: Voice-Activated AI Assistant

Jarvis is a real-time voice assistant that listens to user speech, generates intelligent responses using OpenAI GPT models, 
and speaks the reply back to the user. It combines speech recognition, natural language processing, and text-to-speech to 
create an immersive conversational AI experience.


## Features
- **Voice Input** — Listens to spoken commands via microphone.
- **Speech Recognition** — Converts speech to text using Google Web Speech API.
- **AI Response Generation** — Uses OpenAI GPT-3/4 for contextual responses.
- **Text-to-Speech** — Converts AI responses to audio using `pyttsx3`.
- **Local Model Support** — Loads GPT-2 from Hugging Face as a fallback or for experimentation.
- **Hands-Free Mode** — Runs continuously, enabling always-on interaction.


## Tech Stack
- Python 3.8+
- OpenAI API (GPT-3/4)
- Hugging Face Transformers (GPT-2)
- PyTorch
- SpeechRecognition
- pyttsx3
- Google Web Speech API

## How It Works
1. **Voice Input** – The user speaks into their microphone.
2. **Speech Recognition** – Audio is transcribed into text using a speech-to-text engine.
3. **Natural Language Processing** – The transcribed text is processed through a GPT-powered AI model for contextual understanding and intelligent responses.
4. **Task Execution** – Jarvis can perform commands such as web searches, opening applications, fetching data, and more.
5. **Text-to-Speech Output** – Responses are converted back into natural-sounding speech and played for the user.  

## Potential Use Cases
- **Personal Productivity** – Schedule reminders, set timers, open documents, and automate daily tasks through voice commands.
- **Research Assistance** – Ask questions, summarize articles, or pull in live data without breaking workflow.
- **Entertainment** – Engage in casual conversation, trivia, or storytelling.
- **Smart Home Integration** – Control connected devices via voice commands (future expansion).
- **Hands-Free Computing** – Useful for situations where typing is inconvenient or impossible.
