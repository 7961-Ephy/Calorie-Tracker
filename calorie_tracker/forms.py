from django import forms
from .models import Food, CalorieEntry

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories']

class CalorieEntryForm(forms.ModelForm):
    class Meta:
        model = CalorieEntry
        fields = ['food']