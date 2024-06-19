from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = forms.CharField(max_length=6)

class SyntaxIdentificationForm(forms.Form):
    answer = forms.CharField(label='Your Guess:', max_length=100)


class SurveyForm(forms.Form):
    rating_scale_choices = [(i, str(i)) for i in range(1, 11)]

    overall_experience = forms.ChoiceField(
        choices=rating_scale_choices,
        widget=forms.RadioSelect,
        label="On a scale of 1-10, how would you rate your overall experience with our website?"
    )
    technical_issues = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Were there any technical issues or errors during the assessment?"
    )
    satisfaction = forms.ChoiceField(
        choices=rating_scale_choices,
        widget=forms.RadioSelect,
        label="How would you rate the overall satisfaction with your assessment experience?"
    )
    challenges = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Did you face any challenges while using our website?"
    )
    assessment_quality = forms.ChoiceField(
        choices=rating_scale_choices,
        widget=forms.RadioSelect,
        label="How would you rate the overall quality of the assessment?"
    )
    website_changes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label="What changes would you like to see in our website?"
    )