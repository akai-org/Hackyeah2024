from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Chat, Session, Message, Answers
from .serializers import ChatSerializer, SessionSerializer, MessageSerializer, AnswersSerializer



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