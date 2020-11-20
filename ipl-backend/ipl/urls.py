from django.urls import path

from . import views

urlpatterns = [
    path('seasons/', views.seasons, name='seasons'),
    path('statistics/', views.statistics, name='statistics'),
    path('charts/', views.charts, name='charts'),
]
