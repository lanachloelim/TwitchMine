# TwitchMine

**TwitchMine**! A Python script that collects, sanitizes, and stores Twitch chat messages in a MongoDB collection. It currently follows 5 of the top Twitch channels (**KaiCenat, PokiMane, Jynxzi, CaseOh, JasonTheWeen**).

## 📦 Features

- ✅ Recording Twitch chat messages in real-time  
- 🔒 Privacy-safe (username hashing, URL sanitization) 
- 🗂 Data organized by channel
- ⚙️ **Ideal for training LLMs**

## 📜 Components

### `chat_listener.py`

A script that uses the [TwitchIO](https://twitchio.dev/) library to:
- Detect when a channel is live and start listening
- Hash usernames (`SHA256`) and sanitize messages (replace with '<URL>' / '@<USER>')
- Organize data by `channel` : { `session_start`, `timestamp`, `username`, and `content` } and stored in a MongoDB collection

## 🚀 Getting Started

This project runs in a virtual environment (AWS EC2 instance) and writes to a cloud database (MongoDB Atlas).

## 📞 Contact

If you find any bugs or have questions/suggestions, feel free to contact me (lanachloelim@gmail.com)!


