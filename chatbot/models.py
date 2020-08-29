from django.db import models

# Create your models here.
class ChatBot(models.Model):
    classes=models.FileField(upload_to='Model')
    intents=models.FileField(upload_to='Model')
    words=models.FileField(upload_to='Model')
    chatbot_model=models.FileField(upload_to='Model')

