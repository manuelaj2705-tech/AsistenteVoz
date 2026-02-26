import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversión de Texto a Audio")
image = Image.open('ASISTENTE.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Esrcibe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("¿ Qué es un asistente de voz")
st.write("""
Un asistente de voz es una tecnología que permite interactuar con dispositivos usando la voz.
Reconoce lo que dices, lo interpreta y responde realizando acciones como buscar información, controlar dispositivos,
enviar mensajes o dar recomendaciones, haciendo más fácil y rápida la interacción sin necesidad de usar las manos.
""")

st.markdown("Quieres escucharlo?, copia el texto")
text = st.text_area("Ingrese El texto a escuchar.")

tld = 'com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English")
)

if option_lang == "Español":
    lg = 'es'
if option_lang == "English":
    lg = 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href

    st.markdown(
        get_binary_file_downloader_html("audio.mp3", file_label="Audio File"),
        unsafe_allow_html=True
    )

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
