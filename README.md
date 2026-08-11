## Introduction
**InterviewGPT**: A real-time AI-powered interview preparation application built with Groq and Llama 3.

## 🚀 Live Demo (Free & Online)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/MukulDhanjal/InterviewGPT)

**👉 Try the live app here: [https://huggingface.co/spaces/MukulDhanjal/InterviewGPT](https://huggingface.co/spaces/MukulDhanjal/InterviewGPT)**

---

## Video Demo
Click on the thumbnail to watch the demo.<br>
<a href="https://youtu.be/26__rpg5AvA">
[![Demo](https://github.com/snehitvaddi/InterviewGPT/blob/main/ApplicationDemo.gif?raw=true)](https://github.com/snehitvaddi/InterviewGPT/blob/main/ApplicationDemo.mp4.mp4?raw=true)
</a>

## Features
- 💬 Real-time AI interview practice with Groq & Llama 3
- 🎯 Practice behavioral, technical & situational questions
- 📝 Detailed feedback on answers using the STAR method
- 🚀 Full mock interview simulation
- 🔐 Secure API Key handling via client browser (localStorage)

## Local Setup (Python / Streamlit Version)
```bash
pip install -r requirements.txt
pip install pyaudio   # required for local audio capture
python -m spacy download en_core_web_sm
```

Set environment variables:
```bash
export GROQ_API_KEY='Your_Groq_API_Key'
export ASSEMBLY_AI_API_KEY='Your_AssemblyAI_API_Key'
```

Run locally:
```bash
streamlit run app.py
```

## Technologies Used
- **LLM Engine**: Groq API (Llama 3)
- **Audio Capture / STT**: AssemblyAI (Local Streamlit mode)
- **Web App**: Vanilla HTML5/CSS3/JS (Hugging Face Static Deployment) & Streamlit (Local)
