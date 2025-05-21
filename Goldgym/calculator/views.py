from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import CalorieProfileForm
from .models import CalorieProfile



User = get_user_model()


def calorie_calculator(request):
    profile = None
    initial_data = {}

    if request.user.is_authenticated:
        try:
            profile = request.user.calorie_profile
        except CalorieProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        form = CalorieProfileForm(request.POST, instance=profile)
        if form.is_valid():
            if request.user.is_authenticated:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('calculator:result')
            else:
                temp_profile = form.save(commit=False)
                temp_profile.bmr = temp_profile.calculate_bmr()
                temp_profile.daily_calories = temp_profile.calculate_daily_calories()
                temp_profile.target_calories = temp_profile.calculate_target_calories()

                request.session['bmr'] = round(temp_profile.bmr)
                request.session['daily_calories'] = round(temp_profile.daily_calories)
                request.session['target_calories'] = round(temp_profile.target_calories)
                request.session['age'] = temp_profile.age
                request.session['height'] = temp_profile.height
                request.session['weight'] = temp_profile.weight
                request.session['gender'] = temp_profile.gender
                request.session['activity_level'] = temp_profile.activity_level
                request.session['goal'] = temp_profile.goal

                return redirect('calculator:result')
    else:
        form = CalorieProfileForm(instance=profile)

    return render(request, 'calculator/calculator.html', {'form': form})


def result(request):
    if request.user.is_authenticated:
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
    else:
        bmr = request.session.get('bmr')
        daily_calories = request.session.get('daily_calories')
        target_calories = request.session.get('target_calories')

        age = request.session.get('age')
        height = request.session.get('height')
        weight = request.session.get('weight')
        gender = request.session.get('gender')
        activity_level = request.session.get('activity_level')
        goal = request.session.get('goal')

        if None in [bmr, daily_calories, target_calories, age, height, weight, gender, activity_level, goal]:
            return redirect('calculator:calculator')

        GENDER_DISPLAY = dict(CalorieProfile.GENDER_CHOICES)
        ACTIVITY_DISPLAY = dict(CalorieProfile.ACTIVITY_LEVEL_CHOICES)
        GOAL_DISPLAY = dict(CalorieProfile.GOAL_CHOICES)

        profile_data = {
            'age': age,
            'height': height,
            'weight': weight,
            'gender': gender,
            'activity_level': activity_level,
            'goal': goal,
            'get_gender_display': GENDER_DISPLAY.get(gender, gender),
            'get_activity_level_display': ACTIVITY_DISPLAY.get(activity_level, activity_level),
            'get_goal_display': GOAL_DISPLAY.get(goal, goal),
        }

        context = {
            'profile': profile_data,
            'bmr': bmr,
            'daily_calories': daily_calories,
            'target_calories': target_calories,
        }

    return render(request, 'calculator/result.html', context)
