import speech_recognition as sr
from pydub import AudioSegment
import os

# Convert MP3 to WAV using pydub
def mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

# Recognize speech using the SpeechRecognition library
def wav_to_text(wav_path, language = 'pl-PL'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)

        return text.toLowerCase()
        


def mp3_to_text(mp3_path):
    temp = 'temp.wav'
    mp3_to_wav(mp3_path,temp)
    wav_to_text(temp)


# Example usage
