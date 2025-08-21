# English Learning & IT Assessment Telegram Bot  

A Telegram bot designed to help users **learn and practice English**, with a strong focus on **conversational skills** and **technical IT interview preparation**.  

---

## ✨ Features  

- 🎙 **Voice-to-Text**  
  Send voice messages, and the bot transcribes them into English text.  

- 📝 **Automatic Text Correction**  
  Grammar, sentence structure, and word choice are corrected while preserving the original meaning.  

- 📊 **Automatic Scoring (0–100)**  
  - **English Score** – evaluates grammar, fluency, and clarity of the original text.  
  - **Context/Technical Score** – measures relevance and technical accuracy, especially for IT-related questions.  

- 🎲 **Random Question Generator**  
  Users can request random questions from predefined conversation sets based on their package or level.  

- 🗄 **Database Integration**  
  Stores user data, conversation sets, transcripts, and scores for continuous evaluation and progress tracking.  

- 💬 **Interactive Feedback**  
  Correction results, transcripts, and scores are returned in a **readable HTML-styled format** inside Telegram.  

---

## 🚀 Use Cases  

- **English Conversation Practice** – Improve fluency and accuracy in daily conversations.  
- **IT Interview Simulation** – Practice technical English and prepare for IT-related job interviews.  

---

## 🛠 Tech Stack  

- **Telegram Bot API**  
- **Speech-to-Text & NLP models** (for transcription & correction)  
- **Database** (to store users, transcripts, scores, and question sets)  
- **HTML rendering** for styled feedback in Telegram  

---

## 📦 Requirements  

Install dependencies with:  

```bash
pip install -r requirements.txt
```
```
aiomysql==0.2.0
python-telegram-bot==22.3
redis==6.2.0
requests==2.32.4
SQLAlchemy==2.0.41
```

---

## 📌 Roadmap  

- [ ] Add AI-powered personalized feedback.  
- [ ] Support for multiple difficulty levels in questions.  
- [ ] Expand conversation sets beyond IT (business, casual, academic).  
- [ ] Analytics dashboard for user progress tracking.  

---

## 📖 License  

This project is licensed under the **MIT License** – feel free to use, modify, and share.  

---
