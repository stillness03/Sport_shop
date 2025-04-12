from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CalorieProfileForm
from .models import CalorieProfile

User = get_user_model()

@login_required
def calorie_calculator(request):
    try:
        profile = request.user.calorie_profile
    except CalorieProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = CalorieProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('calculator:result')
    else:
        form = CalorieProfileForm(instance=profile)

    return render(request, 'calculator/calculator.html', {'form': form})


@login_required
def result(request):
    try:
        profile = request.user.calorie_profile
    except CalorieProfile.DoesNotExist:
        return redirect('calculator:calculator')

    context = {
        'profile': profile,
        'bmr': round(profile.bmr),
        'daily_calories': round(profile.daily_calories),
        'target_calories': round(profile.target_calories),
    }

    return render(request, 'calculator/result.html', context)
