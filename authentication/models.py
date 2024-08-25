from django.db import models 
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model): 
    text = models.CharField(max_length=255) 
 
    def str(self): 
        return self.text 
 
class Option(models.Model):     
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False) 
 
    def str(self): 
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    date_attempted = models.DateTimeField(default=timezone.now)
    # Additional fields as needed, e.g., timestamp

    def str(self):
        return f"{self.user.username}'s Quiz Attempt"
    
class CodeSnippet(models.Model):
    code = models.TextField()
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language

class SurveyResponse(models.Model): 
    overall_experience = models.IntegerField() 
    technical_issues = models.TextField() 
    overall_satisfaction = models.IntegerField() 
    challenges_faced = models.TextField() 
    assessment_quality = models.IntegerField() 
    changes_request = models.TextField() 
 
    def __str__(self): 
        return f'Survey Response {self.id}'

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()  # Now, we will manually set the date
    attended = models.BooleanField(default=False)  # Mark as False initially

    def __str__(self):
        return f"{self.user.username} - {self.date} - {'Present' if self.attended else 'Absent'}"

        