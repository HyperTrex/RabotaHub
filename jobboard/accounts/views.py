from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user_type = request.POST['user_type']
        company_name = request.POST.get('company_name', '').strip()
        context['form_data'] = {
            'username': username,
            'user_type': user_type,
            'company_name': company_name,
        }

        if User.objects.filter(username__iexact=username).exists():
            context['error'] = 'username_exists'
            return render(request, 'accounts/register.html', context)

        user = User.objects.create_user(username=username, password=password)

        from .models import Profile
        Profile.objects.create(
            user=user,
            user_type=user_type,
            company_name=company_name if user_type == 'employer' else ''
        )

        return redirect('login')

    return render(request, 'accounts/register.html', context)


def user_login(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'job_list'
    context = {'next': next_url}

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(next_url)

        context['error'] = 'invalid_login'
        context['username'] = username

    # Add user_type to context if authenticated
    if request.user.is_authenticated:
        try:
            context['user_type'] = request.user.profile.user_type
        except:
            pass

    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')
