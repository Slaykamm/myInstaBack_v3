from datetime import timedelta
from email.message import Message
from celery import shared_task
import time
from storage.models import *
from django.core.mail import send_mail



@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def sendDaylyEmails():

    users = User.objects.all()
    userToEmails = set()

    for user in users:
        userLoginDate = user.last_login
        usersRooms = PrivateRoom.objects.filter(privateRoomMembers=user.id)    # получаем все комнаты юзера
        if usersRooms.exists():
            for room in usersRooms:    
                                    #### перебираем комнаты
                roomMessages = PrivateMessage.objects.filter(privateRoom=room.id).exclude(author=user.id)   #### получаем все сообщения комнаты
                if roomMessages.exists():
                    if abs(roomMessages.last().create_at - userLoginDate) > timedelta(hours=24):  # change to hours=24
                        userToEmails.add(user.id)


    for user in userToEmails:
        try:
            email = User.objects.get(id=user).email
            name = User.objects.get(id=user).username
            send_mail(
                subject='Notify for unread messages at SLN chat',
                message=f'Good day {name}!\n You have unread messages at SLN chat from users.\n',
                from_email='slnconnects@mail.ru',
                recipient_list=[email],
                fail_silently=False,
            )
        except: 
            print(f'отправка {name} сообщения не удалась')   






        #print('userID', user.id)
    # //  получаем все мессаджи 
    # //  фильтруем на мессаджи, которые не автора. 
    # //  сортируем их по дате.
    # //  получаем дату последнего захода в комнату
    # //  филтруем и возвращаем список мессаджей не автора после даты последнего захода
    # //  возвращаем длинну (это будет кол во сообщений)