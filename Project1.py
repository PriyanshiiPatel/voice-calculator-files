import streamlit as st
import speech_recognition as sr
from sympy import sympify, SympifyError
from PIL import Image

# App Configuration
st.set_page_config(page_title="PyVoiceCalc", layout="centered")

# Title and Description
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎙 PyVoiceCalc</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>A smart voice-controlled calculator for complex expressions</h4>", unsafe_allow_html=True)
st.write("---")

# Instructions
st.write("""
📌 Click the button below and speak an arithmetic expression clearly.
You can use operators like *plus, **minus, **times, **divided by, **raised to*, etc.
You can also use parentheses by saying "open bracket" and "close bracket".
""")

# Button to start listening
if st.button("Start Listening 🎤"):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎧 Listening... Please speak now.")
            audio = recognizer.listen(source, timeout=10)
            st.info("🔄 Processing...")

            # Convert audio to text
            text = recognizer.recognize_google(audio)
            st.write(f"🗣 *You said:* {text}")

            # Parse text into mathematical expression
            expression = text.lower()
            replacements = {
                "plus": "+",
                "minus": "-",
                "times": "*",
                "multiplied by": "*",
                "into": "*",
                "divided by": "/",
                "over": "/",
                "power of": "",
                "raised to": "",
                "open bracket": "(",
                "close bracket": ")"
            }
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)

            st.write(f"📘 *Parsed expression:* {expression}")

            # Evaluate safely using sympy
            try:
                result = sympify(expression)
                st.success(f"✅ *Result:* {result}")
            except SympifyError:
                st.error("⚠ Invalid expression. Please try again.")
            except Exception as e:
                st.error(f"⚠ Error: {e}")

    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio.")
    except sr.RequestError:
        st.error("❌ Could not request results; check your internet.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")

# Footer
st.write("---")
st.markdown("<p style='text-align: center; color: #777;'>Developed by Your Name | Python Streamlit Project</p>", unsafe_allow_html=True)