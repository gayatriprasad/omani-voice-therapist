import streamlit as st
import requests
import os

st.set_page_config(page_title="Omani Therapist", layout="centered")
st.title(" Omani Voice Therapist")
st.markdown("Speak your mind. We'll respond with empathy and cultural care.")

# --- Session State ---
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_response" not in st.session_state:
    st.session_state.last_response = ""
if "show_continue" not in st.session_state:
    st.session_state.show_continue = False

# --- Voice File Upload ---
uploaded_file = st.file_uploader(" Upload your voice (WAV format)", type=["wav"])
transcribed_text = ""

if uploaded_file:
    st.audio(uploaded_file, format="audio/wav")
    with st.spinner("Transcribing..."):
        try:
            files = {"file": uploaded_file}
            resp = requests.post("http://localhost:8020/transcribe", files=files)
            resp.raise_for_status()
            transcribed_text = resp.json()["text"]
            st.success(f" Transcribed: {transcribed_text}")
        except Exception as e:
            st.error(f"STT failed: {e}")

# --- Text Input Fallback ---
text_input = st.text_input(" Or type your concern:", value=transcribed_text)

# --- User Context ---
st.markdown("####  Contextual Settings")
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["male", "female"])
    family_role = st.selectbox(
        "Family Role",
        ["eldest_son", "younger_son", "eldest_daughter", "younger_daughter"],
    )
with col2:
    religiosity = st.selectbox("Religiosity", ["secular", "moderate", "practicing"])
    honor = st.selectbox("Honor Sensitivity", ["low", "high"])

user_context = {
    "cultural_background": "omani",
    "religiosity_level": religiosity,
    "honor_sensitivity": honor,
    "gender": gender,
    "family_role": family_role,
}

# --- Submit + Full Roundtrip ---
if st.button(" Get Support"):
    if not text_input.strip():
        st.warning("Please enter or upload something first.")
    else:
        with st.spinner("Analyzing and generating response..."):
            try:
                # 1. Generate response
                payload = {"input_text": text_input, "user_context": user_context}
                response = requests.post("http://localhost:8000/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                raw = data["raw_response"]
                adapted = data["culturally_adapted_response"]

                st.markdown(f"** Raw GPT-4o:** {raw}")
                st.markdown(f"** Adapted:** {adapted}")

                # 2. Send to TTS
                tts_resp = requests.post(
                    "http://localhost:8005/speak", json={"text": adapted}
                )
                with open("response.mp3", "wb") as f:
                    f.write(tts_resp.content)
                st.audio("response.mp3", format="audio/mp3")

                st.session_state.last_input = text_input
                st.session_state.last_response = adapted
                st.session_state.show_continue = True
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# --- Followup Button ---
if st.session_state.show_continue:
    st.markdown("---")
    if st.button(" Continue?"):
        st.session_state.last_input = ""
        st.session_state.last_response = ""
        st.session_state.show_continue = False
        st.experimental_rerun()
