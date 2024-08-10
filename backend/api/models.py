from django.db import models

# Create your models here.

class Chat(models.Model):
    class Meta:
        app_label = 'api'
    
    username = models.CharField(max_length=100)
    
    user_text = models.TextField()
    
    bot_text = models.TextField()
    
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.username