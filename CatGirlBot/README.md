# CatBot: Discord Media Responder with Backblaze B2 Integration

CatBot is a Discord bot that listens for specific keywords in messages and responds with random images stored in a Backblaze B2 cloud storage bucket. Designed for automated media delivery, CatBot organizes images into themed folders and serves direct download links in real time.


## Features
- **Keyword Detection** — Listens for custom triggers (`Meow`, `MeowMale`, `Uwu`).
- **Random Media Selection** — Picks a random image from the matched category.
- **Cloud Storage Integration** — Fetches images directly from Backblaze B2.
- **Direct Link Sharing** — Sends accessible image links in Discord channels.
- **Category Support** — Organize media by folder for structured responses.
- **Channel Restrictions** — Only responds in channels containing `"bot"` in their name.


## Tech Stack
- Python 3.8+
- discord.py — Discord API wrapper.
- b2sdk — Backblaze B2 Cloud Storage SDK.
- random — Randomized image selection.
- re — Regular expressions for keyword matching.
- Backblaze B2 Cloud Storage — Media hosting.

## How It Works  
CatBot integrates voice input, AI processing, and voice output for natural, real-time interactions.  

1. **Voice Input** – The user speaks into their microphone. CatBot uses `SpeechRecognition` to transcribe speech into text.  
2. **Language Processing** – The transcribed text is sent to a GPT model, which generates a contextually relevant and conversational response.  
3. **Voice Output** – The response is converted into audio using `pyttsx3`, allowing the bot to “speak” naturally to the user.  
4. **Continuous Conversation** – CatBot listens for follow-up questions or commands, maintaining context for smoother, more human-like interactions.  

## Potential Use Cases  
- **Hands-Free Assistance** – Answer questions or provide information while cooking, driving, or multitasking.  
- **Accessibility Tool** – Enable voice-based communication for users who have difficulty typing.  
- **Language Learning** – Practice speaking and listening skills in a conversational format.  
- **Daily Reminders** – Hear reminders, weather updates, or to-do lists read aloud.  
- **Interactive Entertainment** – Hold casual conversations, tell jokes, or play simple voice-based games.  


