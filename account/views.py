from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages


@login_required
def dashboard(request):
    absolute_url = request.build_absolute_uri('/')
    f_abs_url = f"{absolute_url}?user={request.user.username}"
    print(f_abs_url)
    context = {'abs_url':f_abs_url}
    return render(request, 'account/dashboard.html', context)


def login_user_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('account:dashboard'))  
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                return redirect(reverse('account:dashboard'))  
        else:
            messages.error(request, 'invalid username or password')
            return redirect(reverse('account:login_user')) 
    return render(request, 'login.html')

@login_required
def logout_user_view(request):
    logout(request)
    return redirect(reverse('account:login_user')) 


def search_number_admin(request):
     if request.method == 'POST':
        messages.error(request, 'invalid verification key, please check the key and try again')
        return redirect(reverse('account:dashboard'))  
     return redirect(reverse('account:dashboard'))  
