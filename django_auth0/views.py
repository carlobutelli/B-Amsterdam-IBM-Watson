# -*- coding: utf-8 -*-
from .auth_helpers import process_login
from django.http import HttpResponse


def auth_callback(request):
    return HttpResponse("ciao")
    # return process_login(request)
