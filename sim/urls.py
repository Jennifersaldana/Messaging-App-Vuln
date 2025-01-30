from django.urls import path
from . import views
from .views import upload_file

urlpatterns = [
    path('', views.chat, name='chat'),
    path('create-message/', views.create_message, name='create-message'),
    path('stream-chat-messages/', views.stream_chat_messages, name='stream-chat-messages'),
    path('delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('edit-message/<int:message_id>/', views.edit_message, name='edit_message'),
    path('upload/', upload_file, name='upload_file'),
]

