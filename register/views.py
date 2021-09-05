from django.shortcuts import render, redirect
from . import forms

# Create your views here.
def register(response):
    if response.method == 'POST':
        form = forms.RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = forms.RegisterForm()

    return render(response, 'register.html', { 'form': form })
