from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def login(request, template='accounts/auth.html'):
    return render(request, template)

@login_required
def logout(request):
    return redirect('https://discovery.eu.auth0.com/v2/logout?returnTo=https%3A%2F%2Fdjango-test.eu-gb.mybluemix.net')