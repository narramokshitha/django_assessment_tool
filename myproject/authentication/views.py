# views.py  
from django.shortcuts import render, redirect  
from django.contrib.auth import authenticate, login, logout  
from django.contrib import messages  
from django.contrib.auth.decorators import login_required  
from .forms import SignupForm  
from .models import Question, Option , QuizAttempt, CodeSnippet 
import random  
from .forms import LoginForm  # Import the LoginForm you just defined 
from .utils import generate_random_string 
from django.http import JsonResponse 
from .forms import SyntaxIdentificationForm
  
  
def home(request):  
    return render(request, 'registration/home.html')  
  
def login_view(request): 
    if request.method == 'POST': 
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password'] 
            captcha = form.cleaned_data['captcha'] 
             
            # Validate CAPTCHA 
            if captcha == request.session.get('captcha'): 
                user = authenticate(request, username=username, password=password) 
                if user is not None: 
                    login(request, user) 
                    # Clear CAPTCHA from session after successful login 
                    del request.session['captcha'] 
                    return redirect('dashboard')  # Redirect to dashboard or any desired page 
                else: 
                    messages.error(request, 'Invalid username or password.') 
            else: 
                messages.error(request, 'Invalid CAPTCHA. Please try again.') 
    else: 
        form = LoginForm() 
        # Generate CAPTCHA 
        captcha = generate_random_string(length=6) 
        request.session['captcha'] = captcha  # Store CAPTCHA in session 
     
    context = { 
        'form': form, 
        'captcha': request.session.get('captcha', ''),  # Pass CAPTCHA to the template 
    } 
    return render(request, 'registration/login.html', context) 
 
def refresh_captcha(request): 
    new_captcha = generate_random_string(length=6) 
    request.session['captcha'] = new_captcha 
    return JsonResponse(new_captcha, safe=False) 
 
def signup_view(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  # Use the custom SignupForm  
        if form.is_valid():  
            form.save()  
            username = form.cleaned_data.get('username')  
            messages.success(request, f'Account created for {username}!')  
            return redirect('login')  # Redirect to login page after successful signup  
    else:  
        form = SignupForm()  # Use the custom SignupForm  
    return render(request, 'registration/signup.html', {'form': form})  
  
def logout_view(request):  
    logout(request)  
    messages.success(request, 'You have successfully logged out.')  
    return redirect('login')  


@login_required
def coding_syntax_identification_view(request):
    # Get a random code snippet
    snippets = CodeSnippet.objects.all()
    if snippets:
        code_snippet = random.choice(snippets)
    else:
        code_snippet = None

    if request.method == 'POST':
        form = SyntaxIdentificationForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            # Add logic to check the user's answer and redirect accordingly
            return redirect('success_page')  # Replace with appropriate redirect
    else:
        form = SyntaxIdentificationForm()

    context = {
        'code_snippet': code_snippet.code if code_snippet else "No code snippets available.",
        'form': form,
    }
    return render(request, 'coding_syntax_identification.html', context)
@login_required 
def dashboard_view(request): 
    user = request.user 
    # Fetch recent 3 quiz attempts for the current user 
    recent_quiz_attempts = QuizAttempt.objects.filter(user=user).order_by('-date_attempted')[:3] 
 
    context = { 
        'user': user, 
        'recent_quiz_attempts': recent_quiz_attempts,  # Pass recent quiz attempts to template 
        # Add more context data as needed for your dashboard 
    } 
    return render(request, 'dashboard.html', context) 
 
@login_required  
def assessments_view(request):  
    return render(request, 'assessments.html')  
@login_required 
def timed_quiz_view(request): 
    questions = list(Question.objects.all()) 
    random.shuffle(questions) 
    questions = questions[:3]  # Fetch 3 random questions 
    request.session['question_ids'] = [question.id for question in questions]  # Store question IDs in session 
    return render(request, 'timed_quiz.html', {'questions': questions}) 
 
@login_required 
def submit_quiz(request): 
    if request.method == 'POST': 
        score = 0 
        total_score = 30  # Assuming each question is worth 10 points, total score for 3 questions is 30 
        question_ids = request.session.get('question_ids', []) 
 
        for question_id in question_ids: 
            selected_option_id = request.POST.get(f'question{question_id}') 
            if selected_option_id: 
                selected_option = Option.objects.get(id=selected_option_id) 
                if selected_option.is_correct: 
                    score += 10 
 
        # Create a new QuizAttempt instance and save to database 
        quiz_attempt = QuizAttempt(user=request.user, score=score, total_questions=len(question_ids)) 
        quiz_attempt.save() 
 
        context = { 
            'score': score, 
            'total_score': total_score, 
            'percentage': (score / total_score) * 100 
        } 
        return render(request, 'quiz_result.html', context) 
    return redirect('assessments') 
 
@login_required  
def surveys_view(request):  
    # Implement your surveys logic here  
    return render(request, 'surveys.html')  