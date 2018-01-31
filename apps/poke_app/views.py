from django.shortcuts import render, HttpResponse, redirect
from ..logReg_app.models import User
from .models import Poke

def index(request):
    if 'user' not in request.session:
        return redirect("/main")
    context = {}
    context['user'] = User.objects.get(id = request.session['user'])
    context['users'] = User.objects.all().exclude(id = request.session['user'])
    context['pokes'] = Poke.objects.all()
    context['user_pokes'] = context['pokes'].filter(poked = request.session['user'])
    context['other_users'] = context['user_pokes'].exclude(poked = request.session['user'])
    context['total'] = context['user_pokes'].count()
    context['count'] = len(pokers)
    return render(request, 'poke_app/index.html', context)

def create(request, id):
    poker = User.objects.get(id=request.session['user'])
    poked = User.objects.get(id=id)
    poke = Poke()
    poke.poker = poker
    poke.poked = poked
    poke.counter+=1
    poke.save()
    return redirect('/pokes')

def logout(request):
    request.session.flush()
    return redirect("/main")
