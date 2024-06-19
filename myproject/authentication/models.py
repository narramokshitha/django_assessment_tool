from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model): 
    text = models.CharField(max_length=255) 
 
    def __str__(self): 
        return self.text 
 
class Option(models.Model):     
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False) 
 
    def __str__(self): 
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    date_attempted = models.DateTimeField(default=timezone.now)
    # Additional fields as needed, e.g., timestamp

    def __str__(self):
        return f"{self.user.username}'s Quiz Attempt"

class CodeSnippet(models.Model):
    code = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language