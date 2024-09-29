from gtts import gTTS
import os
# Text to be converted to speech

def tts_from_string(text = "Witamy w serwisie e-rachmistrz gdzie nasz asystent wypełni za ciebie zeznanie podatkowe.", language='pl'):
    output_path = os.path.abspath(__file__).removesuffix("tts.py")+"output.wav"
    if os.path.exists(output_path):
        os.remove(output_path)
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)
    return output_path
    # tts.save("output.wav")
# Create gTTS object

# print(os.path.abspath(__file__).removesuffix("tts.py")+"output.wav")
# Save the audio file
# tts_from_string(text)

# Play the audio (optional)
# os.system("start output.wav")  # Windows
# os.system("afplay output.mp3")  # macOS
# os.system("mpg123 output.mp3")  # Linux
