from django.contrib import admin
from django.urls import path, include
from storage.views import *



urlpatterns = [
    #path('detail/<int:pk>/', AuthorDetailView.as_view()),
    path('create/', VideoCreateView.as_view()),
    path('detail/<int:pk>/', VideoDetailView.as_view()),
    path('detail/<int:pk>/', CommentsDetailView.as_view()),
    path('detail/<int:pk>/', UsersDetailView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
