import pickle
from pathlib import Path
import os
import websockets
import base64
import asyncio
import json
import streamlit as st
import streamlit_authenticator as stauth
from collections import deque

# Optional imports — gracefully degrade in cloud/demo mode
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    from groq import AsyncGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="InterviewGPT", page_icon="🧠", layout="wide")

# --- API KEYS: check st.secrets (HF Spaces / Streamlit Cloud) then env vars (Render/local) ---
def _get_secret(key: str) -> str:
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key, "")

GROQ_API_KEY = _get_secret("GROQ_API_KEY")
ASSEMBLY_AI_API_KEY = _get_secret("ASSEMBLY_AI_API_KEY")

# --- USER AUTHENTICATION ---
names = ["mukul", "vaddi"]
usernames = ["mukul", "vaddi"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "sales_dashboard",
    "abcdef",
    cookie_expiry_days=30,
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:

    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name.upper()}")

    # ---- MAINPAGE ----
    st.title("🧠 InterviewGPT")
    st.markdown("##")

    # --- Cloud / Demo Mode Banner ---
    if not AUDIO_AVAILABLE:
        st.info(
            "ℹ️ **Demo Mode**: This deployment runs without a microphone. "
            "Audio capture requires local installation. See the README to run locally.",
            icon="🎙️",
        )

    # --- Missing API key warnings ---
    if not GROQ_API_KEY:
        st.warning("⚠️ `GROQ_API_KEY` environment variable is not set. AI responses will not work.")
    if not ASSEMBLY_AI_API_KEY:
        st.warning("⚠️ `ASSEMBLY_AI_API_KEY` environment variable is not set. Transcription will not work.")

    if not AUDIO_AVAILABLE or not GROQ_API_KEY or not ASSEMBLY_AI_API_KEY:
        # ---- DEMO / TEXT CHAT MODE ----
        st.markdown("### 💬 Text Chat Mode")
        st.markdown("Since audio or API keys are unavailable, you can type your interview question below:")

        user_input = st.text_area("Your Question:", placeholder="e.g. Tell me about yourself...", height=100)

        if st.button("Ask InterviewGPT"):
            if not GROQ_API_KEY:
                st.error("Please set the `GROQ_API_KEY` environment variable to use AI features.")
            elif user_input.strip():
                import asyncio
                from groq import AsyncGroq

                async def get_response(prompt):
                    client = AsyncGroq(api_key=GROQ_API_KEY)
                    chat_completion = await client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a helpful interview assistant. Help the user prepare for their interview by answering questions, giving feedback, and suggesting improvements."},
                            {"role": "user", "content": prompt},
                        ],
                        model="llama-3.3-70b-versatile",
                        temperature=0.5,
                        max_tokens=500,
                        stream=False,
                    )
                    return chat_completion.choices[0].message.content

                with st.spinner("InterviewGPT is thinking..."):
                    reply = asyncio.run(get_response(user_input))
                st.markdown(f"<span style='color: green;'>**InterviewGPT:**</span> {reply}", unsafe_allow_html=True)
    else:
        # ---- FULL AUDIO MODE (local) ----
        import pyaudio

        client = AsyncGroq(api_key=GROQ_API_KEY)
        auth_key = ASSEMBLY_AI_API_KEY

        if "text" not in st.session_state:
            st.session_state["text"] = "Listening..."
            st.session_state["run"] = False

        FRAMES_PER_BUFFER = 8000
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()

        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
        )

        conversation_history = deque(maxlen=5)
        transcript = []

        def start_listening():
            st.session_state["run"] = True

        def stop_listening():
            with open("conversation.txt", "w") as file:
                file.write("\n".join(transcript))
            st.session_state["run"] = False

        def apply_differential_privacy():
            if not SPACY_AVAILABLE:
                return
            nlp = spacy.load("en_core_web_sm")
            with open("conversation.txt", "r") as file:
                lines = file.readlines()
            user_lines = [
                line[len("User:"):].strip() for line in lines if line.startswith("User:")
            ]
            user_text = "\n".join(user_lines)
            doc = nlp(user_text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE", "DATE", "PHONE"]:
                    user_text = user_text.replace(ent.text, "[REDACTED]")
            with open("conversation_redacted.txt", "w") as file:
                file.write(user_text)

        start, stop = st.columns(2)
        start.button("Start listening", on_click=start_listening)
        stop.button(
            "Stop listening",
            on_click=lambda: [stop_listening(), apply_differential_privacy()],
        )

        URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

        async def send_receive():
            async with websockets.connect(
                URL,
                extra_headers=(("Authorization", auth_key),),
                ping_interval=5,
                ping_timeout=20,
            ) as _ws:
                await asyncio.sleep(0.1)
                session_begins = await _ws.recv()
                print(session_begins)

                async def send():
                    while st.session_state["run"]:
                        try:
                            data = stream.read(FRAMES_PER_BUFFER)
                            data = base64.b64encode(data).decode("utf-8")
                            json_data = json.dumps({"audio_data": str(data)})
                            await _ws.send(json_data)
                        except websockets.exceptions.ConnectionClosedError as e:
                            print(e)
                            assert e.code == 4008
                            break
                        except Exception as e:
                            print(e)
                            assert False, "Not a websocket 4008 error"
                        await asyncio.sleep(0.01)

                async def receive():
                    while st.session_state["run"]:
                        try:
                            result_str = await _ws.recv()
                            result_json = json.loads(result_str)
                            result = result_json.get("text", "")
                            if result_json.get("message_type") == "FinalTranscript":
                                st.session_state["text"] = f"<span style='color: orange;'>User:</span> {result}"
                                st.markdown(st.session_state["text"], unsafe_allow_html=True)
                                transcript.append(f"User: {result}")
                                conversation_history.append({"role": "user", "content": result})

                                if result:
                                    messages = [
                                        {"role": "system", "content": "You are a helpful interview assistant."}
                                    ] + list(conversation_history)
                                    chat_completion = await client.chat.completions.create(
                                        messages=messages,
                                        model="llama-3.3-70b-versatile",
                                        temperature=0.5,
                                        max_tokens=300,
                                        stream=False,
                                    )
                                    reply = chat_completion.choices[0].message.content
                                    conversation_history.append({"role": "assistant", "content": reply})
                                    transcript.append(f"InterviewGPT: {reply}")
                                    st.session_state["chatText"] = f"<span style='color: green;'>InterviewGPT:</span> {reply}"
                                    st.markdown(st.session_state["chatText"], unsafe_allow_html=True)

                        except websockets.exceptions.ConnectionClosedError as e:
                            print(f"WebSocket connection closed: {e}")
                            break
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

                await asyncio.gather(send(), receive())

        asyncio.run(send_receive())
