## Introduction
**InterviewGPT V2**: A real-time Audio Transcription + LLM interview preparation application. Listens to the system's output voice and responds in real time using Groq's Llama3 model and AssemblyAI transcription.

## 🚀 Live Demo
[![Deploy Status](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)](https://interviewgpt.onrender.com)

**👉 [https://interviewgpt.onrender.com](https://interviewgpt.onrender.com)**

> **Login credentials:** `mukul / mukul` or `vaddi / snehit`

> ⚠️ On the free Render tier the service spins down after inactivity — first load may take ~30 seconds.

---

## Video Demo
Click on the thumbnail to watch the demo.<br>
<a href="https://youtu.be/26__rpg5AvA">
[![Demo](https://github.com/snehitvaddi/InterviewGPT/blob/main/ApplicationDemo.gif?raw=true)](https://github.com/snehitvaddi/InterviewGPT/blob/main/ApplicationDemo.mp4.mp4?raw=true)
</a>

## Setup (Local)
```
pip install -r requirements.txt
pip install pyaudio   # required for local audio capture
python -m spacy download en_core_web_sm
```

```
export GROQ_API_KEY='Your_Groq_API_Key'
export ASSEMBLY_AI_API_KEY='Your_AssemblyAI_API_Key'
```

```
streamlit run app.py
```

## Deploy to Render (Cloud)
1. Fork this repository
2. Go to [render.com](https://render.com) → **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Apply**
5. Add environment variables:
   - `GROQ_API_KEY` → your Groq API key
   - `ASSEMBLY_AI_API_KEY` → your AssemblyAI API key
6. Click **Deploy**

## Technologies Used
- **Speech to Text**: AssemblyAI real-time WebSocket API
- **NLP and Response Generation**: Groq API
- **Model**: llama3-8b-8192
- **Web Framework**: Streamlit
- **Security**: Streamlit Authenticator and differential privacy (spaCy NER)

## Features
- 🎙️ Real-time audio to text conversion using AssemblyAI
- 🤖 Intelligent response generation using Groq's powerful AI models
- 💬 Text chat fallback mode on cloud deployments
- 🔐 User authentication for secure access
- 🛡️ Differential privacy: redacts PII (names, orgs, dates) from transcripts
- 🌐 Interactive web interface built with Streamlit

## Prerequisites
- Python 3.7 or higher
- pip
- [Groq API key](https://console.groq.com) (free tier available)
- [AssemblyAI API key](https://www.assemblyai.com) (free tier available)
