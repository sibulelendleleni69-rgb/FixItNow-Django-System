from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Issue
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def dashboard(request):
    issues = Issue.objects.filter(user=request.user)

    context = {
        'total_issues': issues.count(),
        'pending_issues': issues.filter(status='pending').count(),
        'in_progress_issues': issues.filter(status='in_progress').count(),
        'resolved_issues': issues.filter(status='resolved').count(),
    }

    return render(request, 'dashboard.html', context)


@login_required
def report_issue(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')  
        file = request.FILES.get('file')

        Issue.objects.create(
            user=request.user,
            title=title,
            description=description,
            location=location,  
            file=file
        )

        messages.success(request, 'Issue reported successfully.')
        return redirect('my_issues')

    return render(request, 'report_issue.html')


@login_required
def my_issues(request):
    query = request.GET.get('q')
    issues = Issue.objects.filter(user=request.user).order_by('-created_at')

    if query:
        issues = issues.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
        )

    return render(request, 'my_issues.html', {'issues': issues})


@login_required
def delete_issue(request, id):
    issue = get_object_or_404(Issue, id=id, user=request.user)
    issue.delete()
    messages.success(request, 'Issue deleted successfully.')
    return redirect('my_issues')


@login_required
def edit_issue(request, id):
    issue = get_object_or_404(Issue, id=id, user=request.user)

    if request.method == 'POST':
        issue.title = request.POST.get('title')
        issue.description = request.POST.get('description')
        issue.status = request.POST.get('status')
        issue.save()

        messages.success(request, 'Issue updated successfully.')
        return redirect('my_issues')

    return render(request, 'edit.html', {'issue': issue})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')