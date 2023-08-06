from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

def auth_login(request):
    if request.POST:
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None and user.is_active:
            login(request, user)
            
        return HttpResponseRedirect('/')
        
    return render(request, 'djelmah/login.html')

@login_required
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required
def index(request):
    return HttpResponseRedirect('/djelmah')
