from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.


def home(request):
    return render(request, 'core/home.html')


def description(request):
    return render(request, 'core/description.html')


def control_panel(request):
    return render(request, 'core/control_panel.html')


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('')
#     else:
#         form = UserCreationForm()
#
#     context = {'form': form}
#     return render(request, 'registration/register.html', context)
