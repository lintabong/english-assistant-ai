# 🗣️ Telegram English Fluency Bot

This Telegram bot is designed to help users learn and practice English, with a focus on conversational skills and technical IT assessment. The main features of the bot include:

Voice-to-Text: Users can send voice messages, and the bot will transcribe them into English text.

Automatic Text Correction: The bot corrects grammar, sentence structure, and word choice in the user’s transcript while preserving the original meaning.

Automatic Scoring: The bot provides a 0-100 score for:

English Score – the quality of the user’s original English text.

Context/Technical Score – relevance and technical accuracy of the user’s answer, especially for IT-related questions.

Random Question Generator: Users can request a random question from predefined conversation sets according to their package or level.

Database Integration: The bot uses a database to store user data, conversation sets, transcripts, and scores, enabling ongoing evaluation.

Interactive Feedback: Correction results, transcripts, and scores are sent back to users in a readable format, using HTML styling in Telegram.

This bot is particularly useful for IT interview simulations and English conversation practice.

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
