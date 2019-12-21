from django.urls import path
from . import views

urlpatterns = [
    path('p=<int:pg>', views.board, name='br'),
    path('new', views.new_post, name='new_post'),
    path('my', views.my_posts, name='my_post'),
    path('my/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('my/<int:pk>/del/',views.del_post, name='del'),
]