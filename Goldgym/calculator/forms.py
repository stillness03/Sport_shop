from django import forms
from .models import CalorieProfile


class CalorieProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary lifestyle (little or no physical activity)'),
        ('light', 'Light activity (1-3 workouts per week)'),
        ('moderate', 'Moderate activity (3-5 workouts per week)'),
        ('active', 'High activity (6-7 workouts per week)'),
        ('very_active', 'Very high activity (heavy physical work or training 2 times a day)'),
    ]

    GOAL_CHOICES = [
        ('lose_0.5', 'Lose 0.5 kg per week'),
        ('lose_1', 'Lose 1 kg per week'),
        ('lose_2', 'Lose 2 kg per week'),
        ('maintain', 'Maintain weight'),
        ('gain_0.5', 'Gain 0.5 kg per week'),
        ('gain_1', 'Gain 1 kg per week'),
        ('gain_2', 'Gain 2 kg per week'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(),
        label='Gender'
    )

    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Activity Level'
    )

    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Goal'
    )

    class Meta:
        model = CalorieProfile
        fields = ['gender', 'age', 'height', 'weight', 'activity_level', 'goal']
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs.update({'min': 10, 'max': 120})
        self.fields['height'].widget.attrs.update({'min': 100, 'max': 250})
        self.fields['weight'].widget.attrs.update({'min': 30, 'max': 300})
        self.fields['gender'].widget.attrs.update({'class': 'btn-check'})