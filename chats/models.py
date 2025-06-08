from django.db import models
from django.contrib.auth.models import AbstractUser



from django.db import models

class User(AbstractUser):
  
    pass

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
