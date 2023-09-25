import speech_recognition as sr
from pydub import AudioSegment
from tkinter import *
from tkinter import filedialog
from datetime import datetime

def transcribe_audio(audio_path, lang='fr-FR'):
    recognizer = sr.Recognizer()
    audio_data = AudioSegment.from_mp3(audio_path)
    text = ""

    if len(audio_data) > 60000:  # Check if audio is longer than 1 minute
        print("Audio is too long, splitting into chunks...")
        chunks = split_audio(audio_data)

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}...")
            text += transcribe_chunk(recognizer, chunk, lang) + " "
    else:
        print("Processing entire audio...")
        text = transcribe_chunk(recognizer, audio_data, lang)

    return text

def split_audio(audio_data):
    return [audio_data[i:i + 60000] for i in range(0, len(audio_data), 60000)]

def transcribe_chunk(recognizer, audio_chunk, lang):
    audio_data = sr.AudioData(audio_chunk.raw_data, audio_chunk.frame_rate, audio_chunk.frame_width)

    try:
        text = recognizer.recognize_google(audio_data=audio_data, language=lang)
        return text
    except sr.UnknownValueError:
        return "(Could not understand)"
    except sr.RequestError as e:
        return f"(Could not request results; {e})"

def write_transcribed_text(output_file, text):
    # Écrire le texte dans le fichier sans écraser les données existantes
    with open(output_file, "a") as file:
        file.write(text + "\n")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        transcribed_text = transcribe_audio(file_path)
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"transcription_{date_str}.txt"
        write_transcribed_text(output_file, transcribed_text)
        print(f"Transcribed Text: {transcribed_text}")
        print(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the main window
    browse_file()
