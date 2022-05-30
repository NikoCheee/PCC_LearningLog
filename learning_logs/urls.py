"""Визначає юрл паттерни для длч кернінг логс"""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # головна сторінка
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми
    path('topics/', views.topics, name='topics'),
    # # Сторінка, що присвячена окремій темі
    path('topics/<int:topic_id>', views.topic, name='topic'),
    # # Сторінка для додавання нової теми
    path('new_topic/', views.new_topic, name='new_topic'),
    # # новий допис
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # # Сторінка редагування допису
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
]
