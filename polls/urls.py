from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.add_step1, name='add_step1'),
    path('add-step2', views.add_step2, name='add_step2'),
    path('add-step3', views.add_step3, name='add_step3'),
    path('new-author', views.new_author, name='new_author'),
    path('author-list', views.author_list, name='author_list'),
    path('add-authors', views.add_authors, name='add_authors'),
    path('save-paper', views.save_paper, name='save_paper')
]
