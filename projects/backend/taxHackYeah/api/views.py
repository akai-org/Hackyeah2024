from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import pytesseract
from PIL import Image

from .models import Chat, Session, Message, Answers
from .serializers import ChatSerializer, SessionSerializer, MessageSerializer, AnswersSerializer
from pydub import AudioSegment

# Create your views here.
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import os

from .stt import wav_to_text
from .tts import tts_from_string

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = ChatSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = SessionSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = MessageSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AnswersSerializer


class TranscribeAudioView(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        file = request.FILES.get('audio')

        if not file:
            return Response({'error': 'Brak pliku audio.'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.wav'):
            return Response({'error': 'Błędny format pliku. Obsługiwane są tylko pliki WAV.'},
                            status=status.HTTP_400_BAD_REQUEST)

        temp_file_path = f"C:\\Users\\patro\\akai\\Hackyeah2024\\projects\\backend\\taxHackYeah\\tmp\\{file.name}"

        # temp_file_path = "C:\\Users\\patro\\akai\\Hackyeah2024\\projects\\backend\\taxHackYeah\\api\\audio.wav"

        try:
            with open(temp_file_path, 'wb') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            audio = AudioSegment.from_file(temp_file_path)
            audio.export(temp_file_path, format="wav", parameters=["-acodec", "pcm_s16le"])

            text = wav_to_text(temp_file_path)
            response_data = {'transcription': text}
            status_code = status.HTTP_200_OK

        except Exception as e:
            print(e)
            response_data = {'error': 'Nie udało się zrozumieć pliku audio.'}
            status_code = status.HTTP_400_BAD_REQUEST

        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return Response(response_data, status=status_code)


class OCRPhoto(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        file = request.FILES.get('photo.jpg')

        if not file:
            return Response({'error': 'Brak pliku zdjęcia.'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.jpg'):
            return Response({'error': 'Błędny format pliku. Obsługiwane są tylko pliki JPG.'},
                            status=status.HTTP_400_BAD_REQUEST)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        image = Image.open(file)
        image = image.convert('RGB')

        extracted_text = pytesseract.image_to_string(image)
        print(extracted_text)
        return Response({'extracted_text': extracted_text}, status=status.HTTP_200_OK)


class TextAudioView(viewset.ViewSet):
    def post(self, request, *args, **kwargs):
        text =  request.data.get('text')
        path_to_file = tts_from_string(text)
        response_data = path_to_file
        try:
            return Response(response_data,status.HTTP_200_OK)
        except:
            return Response({'error': 'There was a problem with creating response'},
                            status=status.HTTP_400_BAD_REQUEST)
