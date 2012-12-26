#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def logout_vista(request):
	logout(request)
	return HttpResponseRedirect('/login/')