from gtts import gTTS
import os

# Text to be converted to speech
text = "Hello, this is an example of text to speech conversion."

# Create gTTS object
tts = gTTS(text=text, lang='en')

# Save the audio file
tts.save("output.mp3")

# Play the audio (optional)
os.system("start output.mp3")  # Windows
# os.system("afplay output.mp3")  # macOS
# os.system("mpg123 output.mp3")  # Linux
