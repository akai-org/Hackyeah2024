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
      
        if os.path.exists(wav_path):
            os.remove(wav_path)

        return text
        


def mp3_to_text(mp3_path):
    temp = 'temp.wav'
    mp3_to_wav(mp3_path,temp)
    wav_to_text(temp)


# Example usage
mp3_path = "someaudio.mp3"  # Path to the MP3 file
wav_path = "converted_audio.wav"  # Path to save the WAV file

# Convert MP3 to WAV
mp3_to_wav(mp3_path, wav_path)

# Convert WAV to text
text = speech_to_text(wav_path)
print("rower")
print(text)
