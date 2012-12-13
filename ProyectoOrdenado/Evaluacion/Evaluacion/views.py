#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    return HttpResponseRedirect('/login/')
