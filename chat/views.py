from django.shortcuts import render, redirect
from django.http import HttpRequest
import hashlib
from .models import Person



def home(request):
    person_count = Person.objects.all().count()
    return render(request, "home.html", context = {"person_count": person_count})

def chat(request):
    return render(request, "chat.html")