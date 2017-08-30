# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.timezone import now
import datetime


def home(request):
    today = datetime.date.today()
    # load a template, add variable
    return render(request, "taskbuster/index.html",
                  {'today': today, 'now': now()})


def home_files(request, filename):
    # https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/
    return render(request, filename, {}, content_type="text/plain")
