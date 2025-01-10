from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone
from .models import Food, CalorieEntry, DailyGoal
from .forms import FoodForm, CalorieEntryForm

@login_required
def dashboard(request):
    today = timezone.now().date()
    daily_entries = CalorieEntry.objects.filter(
        user=request.user,
        date=today
    ).select_related('food')
    
    total_calories = sum(entry.food.calories for entry in daily_entries)
    
    # Get or create daily goal
    daily_goal, created = DailyGoal.objects.get_or_create(
        user=request.user,
        defaults={'calorie_goal': 2000}
    )
    
    progress = (total_calories / daily_goal.calorie_goal * 100) if daily_goal.calorie_goal > 0 else 0
    
    context = {
        'entries': daily_entries,
        'total_calories': total_calories,
        'daily_goal': daily_goal.calorie_goal,
        'progress': min(progress, 100)  # Cap at 100%
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            
            # Create calorie entry
            CalorieEntry.objects.create(
                user=request.user,
                food=food,
                date=timezone.now().date(),
                time=timezone.now().time()
            )
            
            messages.success(request, 'Food item added successfully!')
            return redirect('dashboard')
    else:
        form = FoodForm()
    
    return render(request, 'add_food.html', {'form': form})

@login_required
def delete_entry(request, entry_id):
    try:
        entry = CalorieEntry.objects.get(id=entry_id, user=request.user)
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
    except CalorieEntry.DoesNotExist:
        messages.error(request, 'Entry not found!')
    
    return redirect('dashboard')

@login_required
def reset_day(request):
    today = timezone.now().date()
    CalorieEntry.objects.filter(user=request.user, date=today).delete()
    messages.success(request, 'Daily log reset successfully!')
    return redirect('dashboard')

class CustomLoginView(LoginView):
    template_name = 'login.html'