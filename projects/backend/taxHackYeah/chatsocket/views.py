from django.shortcuts import render
from functionalities.STT import wav_to_text

# Create your views here.
from pydub import AudioSegment
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

            try:
                text = wav_to_text(temp_file_path)
                response_data = {'transcription': text}
                status_code = status.HTTP_200_OK

            except sr.UnknownValueError:
                response_data = {'error': 'Nie udało się zrozumieć pliku audio.'}
                status_code = status.HTTP_400_BAD_REQUEST

            except sr.RequestError:
                response_data = {'error': 'Błąd połączenia z serwerem transkrypcji.'}
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(response_data, status=status_code)
        else:
            return Response({'error': 'Błędny format dźwięku, lub brak dźwięku'}, status=status.HTTP_400_BAD_REQUEST)



from django.http import FileResponse
from rest_framework.views import APIView
import os

class AudioDownloadView(APIView):
    def get(self, request, *args, **kwargs):
        text = request['']
        # Path to the audio file on the server
        file_path = '/path/to/audio/file/sample.mp3'

        # Open the file in binary mode and return a FileResponse
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type='audio/mpeg')
        
        # Optional: Add Content-Disposition header to specify the file name and prompt download
        response['Content-Disposition'] = f'attachment; filename="sample.mp3"'
        
        return response
