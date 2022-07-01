from django.core.validators import FileExtensionValidator
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save
from django.dispatch import receiver

#added for password change
from rest_framework import serializers



class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, unique=True) #
    avatar = models.ImageField(upload_to='avatar/', max_length = 100, blank=True)
    phone = models.CharField(blank=True, max_length=20, unique=True)  #
    socialAcc = models.BooleanField(default=False, blank=True)
    isEmailConfirmed = models.BooleanField(default=False, blank=True)
    isPhoneConformed = models.BooleanField(default=False, blank=True)
    

    def __str__(self):
        return self.phone



class Video(models.Model):
    title = models.CharField(verbose_name='Name', unique=True, max_length=128) #
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to='video/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])]
    )

    image = models.ImageField(upload_to='preview/', blank=True)
    rating = models.IntegerField(default = 0)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False, blank=True)
    deleted = models.BooleanField(default=False, blank=True)
    

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    def __str__(self):
        return self.title



class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    video = models.ForeignKey(Video,  on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default = 0)
    create_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class CommentsQuotations(models.Model):
    baseComment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    text = models.TextField()
    create_at = models.DateTimeField(blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)   


class PrivateRoom(models.Model):
    privateRoomMembers = models.ManyToManyField(User, blank=True)
    privateChatName = models.CharField(max_length=64)
    lastOpenDate = models.DateTimeField(blank=True)
    privateChat = models.BooleanField(default=True, blank=True)
    name = models.CharField(max_length=64,  blank=True)

    # или сюда дату последнего открывания. Если дата раньше ласт логин то сообщения светим 

    def __str__(self):
        return self.privateChatName

class PrivateMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    privateRoom = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text

