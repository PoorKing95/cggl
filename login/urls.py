from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.tables, name='root'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('regist/', views.regist, name='regist'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('tables/', views.tables, name='tables'),
    path('check/', views.test, name='check'),
]