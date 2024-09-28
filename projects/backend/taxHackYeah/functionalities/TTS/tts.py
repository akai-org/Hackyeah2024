from gtts import gTTS
import os

# Text to be converted to speech
text = "Witamy w serwisie e-rachmistrz gdzie nasz asystent wypełni za ciebie zeznanie podatkowe."

def tts_from_string(text, language='pl'):
    tts = gTTS(text=text, lang=language)
    tts.save("output.wav")
    # tts.save("output.wav")
# Create gTTS object


# Save the audio file
tts_from_string(text)

# Play the audio (optional)
os.system("start output.wav")  # Windows
# os.system("afplay output.mp3")  # macOS
# os.system("mpg123 output.mp3")  # Linux
