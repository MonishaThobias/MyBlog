from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Subscriber
from .forms import BlogPostForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth import login, logout
from .forms import SubscriberForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q

# Create your views here.

def home(request):
    posts = BlogPost.objects.all().order_by('-created_date', '-created_time')[:3]  # Newest posts first
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.save()
            messages.success(request, "Thanks for subscribing!")
            return redirect('home')
        else:
            messages.error(request, "Please enter a valid email.")
    else:
        form = SubscriberForm()
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_date', '-created_time')  # Newest posts first
    signup_form = SignUpForm()
    login_form = AuthenticationForm()
    context = {
        'posts': posts,
         'signup_form': signup_form,
        'login_form': login_form,
    }
    return render(request, 'myblog.html' , context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Signup successful!'})
            else:
                return redirect('blog_list')
        else:
            errors = form.errors.get_json_data()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
    else:
        form = SignUpForm()

    login_form = AuthenticationForm()
    return render(request, 'myblog.html', {
        'signup_form': form,
        'login_form': login_form,
    })


   
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'valid': not User.objects.filter(username__iexact=username).exists(),
        'message': "Username available" if username and not User.objects.filter(username__iexact=username).exists() else "Username taken"
    }
    return JsonResponse(data)

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'valid': not User.objects.filter(email__iexact=email).exists(),
        'message': "Email available" if email and not User.objects.filter(email__iexact=email).exists() else "Email already used"
    }
    return JsonResponse(data)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
            else:
                return redirect('dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = form.errors.get_json_data()
                return JsonResponse({'success': False, 'errors': errors, 'message': 'Invalid login credentials.'})
    else:
        form = AuthenticationForm()

    return render(request, 'blog/login_modal.html', {'form': form})


@login_required
def dashboard(request):
    # You can pass user info or other data here
    return render(request, 'dashboard.html', {})

def logout_view(request):
    logout(request)
    return redirect('blog_list')

def subscribe_ajax(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': "Thanks for subscribing!"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'message': "Invalid request."})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'details.html', {'post': post})

def search(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        try:
            # Try to parse query as date (YYYY-MM-DD format)
            search_date = datetime.strptime(query, "%Y-%m-%d").date()
            results = BlogPost.objects.filter(
                Q(title__icontains=query) | Q(published_date__date=search_date)
            )
        except ValueError:
            # If query is not a valid date, search only by title
            results = BlogPost.objects.filter(title__icontains=query)

    return render(request, "search_result.html", {"query": query, "results": results})