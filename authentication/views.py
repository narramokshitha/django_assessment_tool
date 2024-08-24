# views.py 
from django.db.models import Count
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from .forms import SignupForm 
from .models import Question, Option , QuizAttempt, CodeSnippet, SurveyResponse, Attendance
import random 
from .forms import LoginForm , SurveyForm # Import the LoginForm you just defined
from .utils import generate_random_string
from django.http import JsonResponse
from .forms import SyntaxIdentificationForm
from django.http import HttpResponse
from datetime import datetime
 
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
def surveys_view(request): 
    if request.method == 'POST': 
        form = SurveyForm(request.POST) 
        if form.is_valid(): 
            # Extract cleaned data from the form 
            overall_experience = form.cleaned_data['overall_experience'] 
            technical_issues = form.cleaned_data['technical_issues'] 
            satisfaction = form.cleaned_data['satisfaction'] 
            challenges = form.cleaned_data['challenges'] 
            assessment_quality = form.cleaned_data['assessment_quality'] 
            website_changes = form.cleaned_data['website_changes'] 
 
            # Save survey response to the database 
            SurveyResponse.objects.create( 
                overall_experience=overall_experience, 
                technical_issues=technical_issues, 
                overall_satisfaction=satisfaction, 
                challenges_faced=challenges, 
                assessment_quality=assessment_quality, 
                changes_request=website_changes 
            ) 
 
            # Redirect after successful submission (optional) 
            return redirect('survey-thank-you')  # Replace with your URL name 
 
    else: 
        form = SurveyForm()  # Create an empty form for GET requests 
 
    context = { 
        'form': form 
    } 
    return render(request, 'surveys.html', context) 
 
@login_required 
def survey_thank_you(request): 
    return render(request, 'thankyou.html')

@login_required 
def dashboard_view(request): 
    recent_quiz_attempts = QuizAttempt.objects.filter(user=request.user).order_by('-date_attempted')[:5] 
 
    # Prepare data for chart.js 
    quiz_scores = [attempt.score for attempt in recent_quiz_attempts] 
    quiz_dates = [attempt.date_attempted.strftime('%Y-%m-%d') for attempt in recent_quiz_attempts] 
 
    return render(request, 'dashboard.html', { 
        'recent_quiz_attempts': recent_quiz_attempts, 
        'quiz_scores': quiz_scores, 
        'quiz_dates': quiz_dates, 
    })

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
        total_score = 30
        question_ids = request.session.get('question_ids', [])
        user_answers = {}

        for question_id in question_ids:
            selected_option_id = request.POST.get(f'question{question_id}')
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                user_answers[f'question{question_id}'] = selected_option_id
                if selected_option.is_correct:
                    score += 10

        request.session['user_answers'] = user_answers

        quiz_attempt = QuizAttempt(user=request.user, score=score, total_questions=len(question_ids))
        quiz_attempt.save()

        # Mark attendance for the day
        Attendance.objects.create(user=request.user, attended=True)

        context = {
            'score': score,
            'total_score': total_score,
            'percentage': (score / total_score) * 100
        }
        return render(request, 'quiz_result.html', context)
    return redirect('assessments')

@login_required
def review_quiz(request):
    if 'question_ids' in request.session and 'user_answers' in request.session:
        question_ids = request.session['question_ids']
        user_answers = request.session['user_answers']
        questions = Question.objects.filter(id__in=question_ids)
        review_data = []
        
        for question in questions:
            correct_option = question.options.get(is_correct=True)
            user_selected_option_id = user_answers.get(f'question{question.id}')
            user_selected_option = None
            if user_selected_option_id:
                try:
                    user_selected_option = Option.objects.get(id=user_selected_option_id)
                except Option.DoesNotExist:
                    user_selected_option = None
            review_data.append({
                'question': question.text,
                'correct_answer': correct_option.text,
                'user_answer': user_selected_option.text if user_selected_option else 'No answer selected'
            })
        
        return render(request, 'review_quiz.html', {'review_data': review_data})
    else:
        # Clear session keys to avoid issues
        request.session.pop('question_ids', None)
        request.session.pop('user_answers', None)
        return redirect('timed_quiz')


@login_required
def coding_syntax_identification_view(request):
    # Get a random code snippet
    if 'code_snippet_id' not in request.session:
        # Select a random code snippet from the database
        code_snippet = random.choice(CodeSnippet.objects.all())
        request.session['code_snippet_id'] = code_snippet.id
    else:
        code_snippet = CodeSnippet.objects.get(id=request.session['code_snippet_id'])

    if request.method == 'POST':
        form = SyntaxIdentificationForm(request.POST)
        if form.is_valid():
            guess = form.cleaned_data['answer']
            if guess.lower() == code_snippet.language.lower():
                # Correct guess
                messages.success(request, "Correct! Here's a new snippet.")
                # Delete the current session key to force a new snippet
                del request.session['code_snippet_id']
                return redirect('coding_syntax_identification')
            else:
                # Incorrect guess
                messages.error(request, "Incorrect, try again.")
                return redirect('coding_syntax_identification')
    else:
        form = SyntaxIdentificationForm()

    context = {
        'code_snippet': code_snippet.code,
        'form': form
    }
    return render(request, 'coding_syntax_identification.html', context)

@login_required
def attendance_report(request):
    # Get the current user
    user = request.user
    
    # Get the current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Filter attendance records for the current month and year
    attendance_records = Attendance.objects.filter(user=user, date__month=current_month, date__year=current_year)
    
    # Count total days and attended days for the current month
    total_days = attendance_records.count()
    attended_days = attendance_records.filter(attended=True).count()

    # Calculate attendance percentage
    if total_days > 0:
        attendance_percentage = (attended_days / total_days) * 100
    else:
        attendance_percentage = 0
    
    context = {
        'attendance_records': attendance_records,
        'attendance_percentage': attendance_percentage,
        'current_month': datetime.now().strftime("%B"),
    }
    
    return render(request, 'attendance.html', context)