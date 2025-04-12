from django.db import models
from django.conf import settings


class CalorieProfile(models.Model):
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
        ('lose_0.5', 'Lose 0.5 kg/week'),
        ('lose_1', 'Lose 1 kg/week'),
        ('lose_2', 'Lose 2 kg/week'),
        ('maintain', 'Maintain weight'),
        ('gain_0.5', 'Gain 0.5 kg/week'),
        ('gain_1', 'Gain 1 kg/week'),
        ('gain_2', 'Gain 2 kg/week'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='calorie_profile' )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    age = models.PositiveIntegerField(verbose_name="Age")
    height = models.PositiveIntegerField(verbose_name="Height (cm)")
    weight = models.FloatField(verbose_name="Weight (kg)")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES, verbose_name="Activity level")
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, verbose_name="Goal")

    bmr = models.FloatField(verbose_name="Basal Metabolic Rate (BMR)", blank=True, null=True)
    daily_calories = models.FloatField(verbose_name="Daily calorie intake", blank=True, null=True)
    target_calories = models.FloatField(verbose_name="Target calorie intake", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_bmr(self):
        if self.gender == 'male':
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161


    def calculate_activity_multiplier(self):
        multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very active': 1.9
        }
        return multipliers.get(self.activity_level, 1.2)

    def calculate_daily_calories(self):
        bmr = self.calculate_bmr()
        activity_multiplier = self.calculate_activity_multiplier()
        return round(bmr * activity_multiplier)

    def calculate_target_calories(self):
        daily_calories = self.calculate_daily_calories()
        goal = self.goal

        if self.goal.startswith('lose'):
            kg_per_week = float(self.goal.split('_')[1])
            return round(daily_calories - (kg_per_week * 1100))
        elif self.goal.startswith('gain'):
            kg_per_week = float(self.goal.split('_')[1])
            return round(daily_calories + (kg_per_week * 1100))
        else:  # maintain
            return round(daily_calories)

    def save(self, *args, **kwargs):
        self.bmr = self.calculate_bmr()
        self.daily_calories = self.calculate_daily_calories()
        self.target_calories = self.calculate_target_calories()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Calorie profile for {self.user.username}"

    class Meta:
        verbose_name = "Calorie profile"
        verbose_name_plural = "Calorie Profiles"