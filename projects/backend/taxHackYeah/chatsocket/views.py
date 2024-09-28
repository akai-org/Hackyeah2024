from django.shortcuts import render
from functionalities.STT import wav_to_text

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import os


class TranscribeAudioView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if file and file.name.endswith('wav'):
            temp_file_path = f"/tmp/{file.name}"
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            audio = AudioSegment.from_mp3(temp_file_path)
            wav_file_path = temp_file_path.replace('.mp3', '.wav')
            audio.export(wav_file_path, format="wav")

            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file_path) as source:
                audio_data = recognizer.record(source)

            try:
                transcription = recognizer.recognize_google(audio_data, language="pl-PL")
                response_data = {'transcription': transcription}
                status_code = status.HTTP_200_OK
            except sr.UnknownValueError:
                response_data = {'error': 'Nie udało się zrozumieć pliku audio.'}
                status_code = status.HTTP_400_BAD_REQUEST
            except sr.RequestError:
                response_data = {'error': 'Błąd połączenia z serwerem transkrypcji.'}
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            finally:
                os.remove(temp_file_path)
                if os.path.exists(wav_file_path):
                    os.remove(wav_file_path)

            return Response(response_data, status=status_code)
        else:
            return Response({'error': 'Proszę przesłać plik MP3.'}, status=status.HTTP_400_BAD_REQUEST)