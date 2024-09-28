from django.test import TestCase

# Create your tests here.
import pytest
from .models import Chat, Session, Message, Answers

@pytest.mark.django_db
def test_create_chat():
    chat = Chat.objects.create(message="Hello world")
    assert Chat.objects.count() == 1
    assert chat.message == "Hello world"
    assert chat.created_at is not None

@pytest.mark.django_db
def test_create_session():
    session = Session.objects.create(ssid="session_1234")
    assert Session.objects.count() == 1
    assert session.ssid == "session_1234"
    assert session.created_at is not None
    assert session.closed is False

@pytest.mark.django_db
def test_create_message():
    session = Session.objects.create(ssid="session_1234")
    message = Message.objects.create(session=session, message="Test message")
    assert Message.objects.count() == 1
    assert message.session == session
    assert message.message == "Test message"
    assert message.answered is False
    assert message.created_at is not None

@pytest.mark.django_db
def test_create_answers():
    session = Session.objects.create(ssid="session_1234")
    answer = Answers.objects.create(session=session, answer="This is an answer", mode="fullgpt")
    assert Answers.objects.count() == 1
    assert answer.session == session
    assert answer.answer == "This is an answer"
    assert answer.mode == "fullgpt"
    assert answer.created_at is not None
