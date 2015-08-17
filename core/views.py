from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/steam/')
def register(request):
    user = None
    template_name = 'register.html'
    success_url = '/dashboard/'
    user = request.user
    ll = user.last_login
    dj = user.date_joined
    td = ll-dj
    
    if (td.seconds == 0):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user.username = form.cleaned_data.get('username')
                user.save()
                return HttpResponseRedirect(success_url)
        else:
            form = RegisterForm()
            return render(request, template_name, {'form': form,})    
    else:
        return HttpResponseRedirect(success_url)