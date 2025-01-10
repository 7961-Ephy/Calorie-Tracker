from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-food/', views.add_food, name='add_food'),
    path('delete-entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('reset-day/', views.reset_day, name='reset_day'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
]