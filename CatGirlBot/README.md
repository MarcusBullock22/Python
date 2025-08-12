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



