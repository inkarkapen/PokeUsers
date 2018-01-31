from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.contrib import messages

#/main
def log_reg(request):
    request.session['logged'] = False
    return render(request, 'logReg_app/log_reg.html')

#/signup
def signup(request):
    errors = User.objects.register_validator(request.POST)
    if valid(request, errors) == True:
        user = User.objects.creator(request.POST)
        request.session['logged'] = True
        request.session['user'] = user.id
        return redirect('/pokes')
    else:
        return redirect('/main')
#/login
def login(request):
    errors = User.objects.login_validator(request.POST)
    if valid(request, errors) == True:
        request.session['logged'] = True
        request.session['user'] = User.objects.get(email = request.POST['email']).id
        return redirect('/pokes')
    else:
        return redirect('/main')

def valid(request, errors):
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return False
    else:
        return True