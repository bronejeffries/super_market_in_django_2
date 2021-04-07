from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        try:
            if user is None:
                messages.error(request, 'invalid credentials please try again')
                return render(request, "registration/login.html", context)
            else:
                if user.is_active:
                    redirect_url = None
                    if user.groups.filter(name="cashier").count():
                        #user is a cashier
                        redirect_url = 'cashier:index'
                        
                    if user.groups.filter(name="manager").count():
                        # user is a manager
                        redirect_url = 'manager:index'
                        
                    if redirect_url is not None:
                        request.session['username'] = username
                        request.session.set_expiry(86400)
                        login(request, user)
                        return HttpResponseRedirect(reverse(redirect_url))
                    
                    messages.warning(request, "Unknown group, contact administrator")
                    return render(request, "registration/login.html", context)
                        
                     
                else:
                    messages.warning(request, "Inactive account, contact administrator")
                    return render(request, "registration/login.html", context)       
        except Exception:
            messages.warning(request, "Something wrong with your account, contact administrator")
            return render(request, "registration/login.html", context)

    else:
        return render(request, "registration/login.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))
