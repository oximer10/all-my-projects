from django.urls import path
from . import views
urlpatterns = [
    path('', views.article_list, name='vlog'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('article/like/<int:pk>/', views.toggle_like, name='article_like'),
]
