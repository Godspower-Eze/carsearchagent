from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cars/', views.index, name='cars'),
    path('search/', views.search, name='search')
]
