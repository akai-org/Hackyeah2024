import speech_recognition as sr
from pydub import AudioSegment

# Convert MP3 to WAV using pydub
def mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

# Recognize speech using the SpeechRecognition library
def speech_to_text(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='pl-PL')
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error: Could not request results."

# Example usage
mp3_path = "someaudio.mp3"  # Path to the MP3 file
wav_path = "converted_audio.wav"  # Path to save the WAV file

# Convert MP3 to WAV
mp3_to_wav(mp3_path, wav_path)

# Convert WAV to text
text = speech_to_text(wav_path)
print("rower")
print(text)
