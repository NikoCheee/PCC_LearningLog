from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Зареєструвати нового користувача"""
    if request.method != 'POST':
        # показати порожню форму реєстрації
        form = UserCreationForm()
    else:
        # опрацювати заповнену форму
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Авторизувати користувача та скерувати його на головну сторінку
            login(request, new_user)
            return redirect('learning_logs:index')

    # показатипорожню або недійсну форму
    context = {'form': form}
    return render(request, 'registration/register.html', context)


