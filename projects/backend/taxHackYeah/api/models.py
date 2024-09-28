from django.db import models


class Chat(models.Model):
    objects = models.Manager()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    objects = models.Manager()

    ssid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    objects = models.Manager()

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    message = models.TextField()
    answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message


class Answers(models.Model):
    GPT_CHOICES = [
        ('fullgpt', 'Full GPT'),
        ('lowgpt', 'Low GPT'),
        ('databased', 'Database Model'),
        ("unknown", "Unknown")
    ]
    objects = models.Manager()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=100, choices=GPT_CHOICES, default='unknown')

    def __str__(self):
        return self.answer