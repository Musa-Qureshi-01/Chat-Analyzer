# 📊 Chat Analyzer
**Chat Analyzer is an interactive Streamlit app that turns your raw chat data into beautiful, insightful visualizations.
Analyze activity patterns, top users, word frequency, emoji usage, and more — all in just a few clicks.**

---

## 🚀 Features

- Top Statistics – Total messages, words, media, and links shared
- Activity Trends – Monthly & daily timelines, busiest days & hours
- Most Active Users – See who dominates the conversation
- Word Analysis – WordCloud and most common words
- Emoji Usage – Breakdown of emoji frequency and types
- Interactive Visuals – Built with Plotly, Seaborn, and Matplotlib

## 🛠️ Built With

- Streamlit – Web app framework
- Pandas – Data processing
- Seaborn & Matplotlib – Visualizations
- Plotly Express – Interactive charts
- WordCloud – Word frequency visualization
- emoji – Emoji parsing
- urlextract – Link extraction

---
## 📂 Example Stats

- From a sample dataset:

- Total Messages: 9,861
- Total Words: 65,699
- Media Shared: 1,858
- Links Shared: 330
- Average Words per Message: ~6.6
---

## 📦 Installation & Usage
Clone the repository

git clone https://github.com/yourusername/chat-analyzer.git
cd chat-analyzer
Install dependencies

pip install -r requirements.txt
Run the app

streamlit run app.py
Upload your chat file
Currently supports WhatsApp chat exports (without media).

---

### 📝 How It Works

- Upload Chat File – Export your chat from WhatsApp and upload the .txt file.
- Data Processing – The app extracts timestamps, sender names, messages, links, media, and emojis.
- Visualization – Interactive charts display trends, activity maps, word clouds, and emoji stats.

---

### 📧 Contact
If you have suggestions or questions:
Email: musaqureshi0000@gmail.com

----

## ©️Live Preview - 
- Chat Analyzer: [chat-x-analyzer](https://chat-x-analyzer.streamlit.app/)

---

### ❤️ Acknowledgements
Thanks to the creators of the amazing Python libraries that make this possible.

---
💡 Tip: “Your chats hold stories — let Chat Analyzer help you tell them.”
