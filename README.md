# 🗣️ Telegram English Fluency Bot

A conversational **Telegram Bot** designed to help you practice and improve your **spoken and written English fluency** through interactive chat and voice transcription.  
The bot uses **Google Gemini AI** for language understanding, **MySQL** for persistent storage, and **Redis** for caching.  

---

## ✨ Features
- 📩 **Text Conversation**: Chat with the bot and get AI-powered responses.  
- 🎙️ **Voice Practice**: Send voice messages → bot transcribes → then improves grammar and fluency.  
- 📚 **Fluency Feedback**: Compare your raw transcript vs corrected version.  
- ⚡ **Cache with Redis**: Reduce API calls & improve performance.  
- 🗄️ **MySQL Database**: Store user interactions, progress, and logs for learning analytics.  
- 🔐 **Environment-based Config**: Uses `.env` for secrets and tokens.  

---


## ⚙️ Requirements
- Python **3.10+**
- A **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)  
- A **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com)  
- Running instances of:
  - **MySQL** (for database persistence)  
  - **Redis** (for caching session/context)  

---
