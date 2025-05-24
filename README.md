# TwitchMine

**TwitchMine**! A Python script that collects, sanitizes, and stores Twitch chat messages into SQLite databases. It currently follows 5 of the top Twitch channels (**KaiCenat, PokiMane, Jynxzi, CaseOh, JasonTheWeen**).

---

## 📦 Features

- ✅ Real-time Twitch chat logging  
- 🔒 Privacy-safe (username hashing) 
- 🧹 URL sanitization  
- 🗂 Organized by channel and timestamp  
- 🧪 **Ideal for training LLMs**

---

## 📜 Components

### `chat_listener.py`

A script that uses the [TwitchIO](https://twitchio.dev/) library to:
- Connect to Twitch chat via IRC
- Hash usernames (`SHA256`)
- Strip links from messages
- Store everything in a `.db` file under `data/<channel>/`

### `/data`

Folder structure:

```
data/
├── KaiCenat
│   ├── 20250524005632.db
│   └── ...
├── PokiMane
├── ...
```

### `.db` files

Each `.db` file is labeled by start stream timestamp and contains a table named `messages` with columns for `id`, `timestamp`, `channel`, `user_hash`, and `content`.

---

## 🚀 Getting Started

---

## 📞 Contact

If you find any bugs or have questions/suggestions, feel free to contact me (lanachloelim@gmail.com)!


