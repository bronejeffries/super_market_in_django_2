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
        radio = request.POST['radio']
        user = authenticate(request, username=username, password=password)
        print(username,password)
        print(user)
        try:
            if (user is None):
                # context['error'] = ""
                messages.error(request, 'invalid credentials please try again')
                # return HttpResponseRedirect(reverse('login:login'))
                return render(request, "registration/login.html", { 'messages':messages})
        except Exception:
                context['error'] = "invalid credentials please try again"
                # return HttpResponseRedirect(reverse('login:login'))
                return render(request, "registration/login.html", {'context': context})
        else:
            try:
                getgroupobject = Group.objects.get(name = radio)
                group_1 = user.groups.get(id = getgroupobject.id)
            except Exception:

                messages.error(request, 'Choose the right button please...')
                # return HttpResponseRedirect(reverse('login:login'))
                return render(request, "registration/login.html", {'messages':messages})
            else:
                if user:
                    if getgroupobject.name == 'cashier':
                        if user.is_active:
                            request.session['username'] = username
                            request.session.set_expiry(86400)
                            login(request, user)
                            return HttpResponseRedirect(reverse('cashier:index'))
                    else:

                        if user.is_active:
                            request.session['username'] = username
                            request.session.set_expiry(86400)
                            login(request, user)
                            return HttpResponseRedirect(reverse('manager:index'))

    else:
        return render(request, "registration/login.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))
