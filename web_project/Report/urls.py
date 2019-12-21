from django.urls import path
from . import views

urlpatterns = [
    path('report/create/', views.rep_post, name='rep_post'),
]