from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Food(models.Model):
    name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CalorieEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.date}"

class DailyGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calorie_goal = models.PositiveIntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Goal - {self.calorie_goal} calories"