from rest_framework.reverse import reverse
from venv import create
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework import viewsets
import urllib3
from storage.serializer import VideoDetailSerializer, VideoViewSerializer, AuthorDetailSerializer, AuthorViewSerializer, CommentsDetailSerializer, CommentsViewSerializer, UsersDetailSerializer, UsersViewSerializer 
from storage.serializer import CommentsQuotationsDetailSerializer, CommentsQuotationsViewSerializer, PrivateMessageDetailSerializer, PrivateMessageViewSerializer, PrivateRoomDetailSerializer, PrivateRoomViewSerializer, UserDetailsSerializer
from storage.models import Video, Author, Comments, User, CommentsQuotations, PrivateMessage, PrivateRoom
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

import urllib


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import VKProvider


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from django.contrib.auth import get_user_model

global userData



userData = {}



USER_FIELDS = [
    "first_name",
    "last_name",
    "nickname",
    "screen_name",
    "sex",
    "bdate",
    "city",
    "country",
    "timezone",
    "photo",
    "photo_medium",
    "photo_big",
    "photo_max_orig",
    "has_mobile",
    "contacts",
    "education",
    "online",
    "counters",
    "relation",
    "last_seen",
    "activity",
    "universities",
]


class VKOAuth2Adapter(OAuth2Adapter):
    provider_id = VKProvider.id
    access_token_url = "https://oauth.vk.com/access_token"
    authorize_url = "https://oauth.vk.com/authorize"
    profile_url = "https://api.vk.com/method/users.get"

    def complete_login(self, request, app, token, **kwargs):
        uid = kwargs["response"].get("user_id")
        params = {
            "v": "5.95",
            "access_token": token.token,
            "fields": ",".join(USER_FIELDS),
        }
        if uid:
            params["user_ids"] = uid
        resp = requests.get(self.profile_url, params=params)
        resp.raise_for_status()
        extra_data = resp.json()["response"][0]
        email = kwargs["response"].get("email")
        if email:
            extra_data["email"] = email
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(VKOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VKOAuth2Adapter)

class VkConnect(SocialLoginView):
    client_class = OAuth2Client
    adapter_class = VKOAuth2Adapter

    @property
    def callback_url(self):
        return self.request.build_absolute_uri(reverse('vk_callback'))


def vk_callback(request):
    params = urllib.parse.urlencode(request.GET)
    #global userData
    #userData = {'accessToken': params}
    return redirect(f'http://localhost:3000/login/${params}')




def vk_userDatacallback(request):
    params = urllib.parse.urlencode(request.GET)
    global userData
    params = userData
    return redirect(f'http://localhost:3000/retrieveName/{params}')




from allauth.account.signals import user_logged_in
def user_logged_in_receiver(request, user, **kwargs):
    global userData
    userData = user

    testUserExist = User.objects.filter(username=user)
    if len(testUserExist):
        isAuthor = Author.objects.filter(name=User.objects.get(username=user).id)
        if not len(isAuthor):
            Author.objects.create(name=User.objects.get(username=user), socialAcc=True)

user_logged_in.connect(user_logged_in_receiver, sender=User)



# =============BLOCK FOR PASSWORD CHANGING
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import ChangePasswordSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##==================END==============

#Author

##ниже 2 класса аокнментил. тестю.
class AuthorCreateView(generics.CreateAPIView):
    serializer_class =  AuthorDetailSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorDetailSerializer
    queryset = Video.objects.all()    


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()

    serializer_class = AuthorViewSerializer

    def get_queryset(self, **kwargs):
            id =  self.request.query_params.get('id', None)
            name = self.request.query_params.get('name', None)  
            email =  self.request.query_params.get('email', None)

            if id:
                return Author.objects.filter(id=id)
            elif name:
                return Author.objects.filter(name=name)
            elif email:
                return Author.objects.filter(email=email)
            else:
                return Author.objects.all()


    def save(self, *args, **kwargs):
        # Сначала модель нужно сохранить, иначе изменять/обновлять будет нечего
        super(Author, self).save(*args, **kwargs)


    def post(self, request, *args, **Kwargs):
        
        if len(request.FILES) !=0:
            file = request.FILES['imagefile']
            print('request.FILES', request.FILES)
            print('file', file)

            idd = self.kwargs['pk']
            newImageToBase = Author.objects.get(id = idd)
            print("000", idd, newImageToBase.name)

            newImageToBase.avatar = request.FILES['imagefile']
            newImageToBase.save()

        return HttpResponse({'message':'Avatar added'}, status = 200)



#Video
class VideoCreateView(generics.CreateAPIView):
    serializer_class =  VideoDetailSerializer


class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoDetailSerializer
    queryset = Video.objects.all()    

class VideoViewSet(viewsets.ModelViewSet):

    queryset = Video.objects.all()
    serializer_class = VideoViewSerializer
  #  permission_classes=[IsAuthenticated]

    def get_queryset(self, **kwargs):
            id =  self.request.query_params.get('id', None)
            title = self.request.query_params.get('title', None)  
            author =  self.request.query_params.get('author', None)
            rating = self.request.query_params.get('rating', None)  
            create_at = self.request.query_params.get('create_at', None)  


            if id:
                return Video.objects.filter(id=id)
            elif title:
                return Video.objects.filter(title=title)
            elif author:
                return Video.objects.filter(author=author)
            elif rating:
                return Video.objects.filter(rating=rating)
            elif create_at:
                return Video.objects.filter(create_at=create_at)

            else:
                return Video.objects.all()

    def post(self, request, *args, **Kwargs):
        
        if len(request.FILES) !=0:
            idd = self.kwargs['pk']
            newImageToBase = Video.objects.get(id = idd)


            if 'imagefile' in request.FILES:
                file = request.FILES['imagefile']
                newImageToBase.image = request.FILES['imagefile']
                newImageToBase.save()
            else:
                file = request.FILES['videofile']
                if file:
                    newImageToBase.video = request.FILES['videofile']
                    newImageToBase.save()

        return HttpResponse({'message':'Video Preview added'}, status = 200)

#Comments

class CommentsCreateView(generics.CreateAPIView):
    serializer_class =  CommentsDetailSerializer


class CommentsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentsDetailSerializer
    queryset = Comments.objects.all()    


class CommentsViewSet(viewsets.ModelViewSet):
   #permission_classes=[IsAuthenticated]
   queryset = Comments.objects.all()

   serializer_class = CommentsViewSerializer

   def get_queryset(self, **kwargs):
        id =  self.request.query_params.get('id', None)
        author =  self.request.query_params.get('author', None)
        video = self.request.query_params.get('video', None)  
        rating = self.request.query_params.get('rating', None)  
        create_at = self.request.query_params.get('create_at', None)  


        if id:
            return Comments.objects.filter(id=id)

        elif author:
            return Comments.objects.filter(author=author)

        elif video:
            return Comments.objects.filter(video=video)

        elif rating:
            return Comments.objects.filter(rating=rating)

        elif create_at:
            return Comments.objects.filter(create_at=create_at)
            
        else:
            return Comments.objects.all()


##--------------------QUAOTATIONSSSSSSSSSSSS
class CommentsQuotationsViewSet(viewsets.ModelViewSet):
   #permission_classes=[IsAuthenticated]
   queryset = CommentsQuotations.objects.all()

   serializer_class = CommentsQuotationsViewSerializer

   def get_queryset(self, **kwargs):
        id =  self.request.query_params.get('id', None)
        baseComment =  self.request.query_params.get('baseComment', None)
        author = self.request.query_params.get('author', None)  
        text = self.request.query_params.get('text', None)  
        create_at = self.request.query_params.get('create_at', None)  


        if id:
            return CommentsQuotations.objects.filter(id=id)

        elif baseComment:
            return CommentsQuotations.objects.filter(baseComment=baseComment)

        elif author:
            return CommentsQuotations.objects.filter(author=author)

        elif text:
            return CommentsQuotations.objects.filter(text=text)

        elif create_at:
            return CommentsQuotations.objects.filter(create_at=create_at)

        else:
            return CommentsQuotations.objects.all()




# ------------------------------USERS----------------

class UsersCreateView(generics.CreateAPIView):
    serializer_class =  UsersDetailSerializer


class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsersDetailSerializer
    queryset = User.objects.all()    
    

class UsersViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UsersViewSerializer
   #permission_classes=[IsAuthenticated]

   def get_queryset(self, **kwargs):
        id =  self.request.query_params.get('id', None)
        password =  self.request.query_params.get('password', None)
        username = self.request.query_params.get('username', None)  
        first_name = self.request.query_params.get('first_name', None)  
        last_name = self.request.query_params.get('last_name', None)  
        email = self.request.query_params.get('email', None)  
        date_joined = self.request.query_params.get('date_joined', None)  
        groups = self.request.query_params.get('groups', None)  

        if id:
            return User.objects.filter(id=id)

        elif password:
            return User.objects.filter(password=password)

        elif username:
            return User.objects.filter(username=username)

        elif first_name:
            return User.objects.filter(first_name=first_name)

        elif last_name:
            return User.objects.filter(last_name=last_name)

        elif email:
            return User.objects.filter(email=email)

        elif date_joined:
            return User.objects.filter(date_joined=date_joined)

        elif groups:
            return User.objects.filter(groups=groups)

        else:
            return User.objects.all()




# ------------------------------Message Rooms--------- PrivateRoom-------

class PrivateRoomCreateView(generics.CreateAPIView):
    serializer_class =  PrivateRoomDetailSerializer


class PrivateRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateRoomDetailSerializer
    queryset = PrivateRoom.objects.all()    

class PrivateRoomViewSet(viewsets.ModelViewSet):
   queryset = PrivateRoom.objects.all()
   serializer_class = PrivateRoomViewSerializer
   #permission_classes=[IsAuthenticated]

   def get_queryset(self, **kwargs):
        id =  self.request.query_params.get('id', None)
        privateRoomMembers =  self.request.query_params.get('privateRoomMembers', None)
        privateChatName = self.request.query_params.get('privateChatName', None)  

        if id:
            return PrivateRoom.objects.filter(id=id)

        elif privateRoomMembers:
            return PrivateRoom.objects.filter(privateRoomMembers=privateRoomMembers)

        elif privateChatName:
            return PrivateRoom.objects.filter(privateChatName=privateChatName)

        else:
            return PrivateRoom.objects.all()

   def post(self, request, *args, **Kwargs):
        print('ya tutta request', request)
        id = self.kwargs['pk']
        print('ya tutta', id)
        if PrivateRoom.objects.filter(id=id).exists():
            return PrivateRoom.objects.filter(id=id)
        # else:
        #     PrivateRoom.objects.create(privateChatName=) 





# ------------------------------Message Rooms--------- PrivateMessage-------

class PrivateMessageCreateView(generics.CreateAPIView):
    serializer_class =  PrivateMessageDetailSerializer


class PrivateMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateMessageDetailSerializer
    queryset = PrivateMessage.objects.all()    

class PrivateMessageViewSet(viewsets.ModelViewSet):
   queryset = PrivateMessage.objects.all()
   serializer_class = PrivateMessageViewSerializer
   #permission_classes=[IsAuthenticated]

   def get_queryset(self, **kwargs):
        id =  self.request.query_params.get('id', None)
        author =  self.request.query_params.get('author', None)
        text = self.request.query_params.get('text', None)  
        privateRoom = self.request.query_params.get('privateRoom', None)  

        if id:
            return PrivateMessage.objects.filter(id=id)

        elif author:
            return PrivateMessage.objects.filter(author=author)

        elif text:
            return PrivateMessage.objects.filter(text=text)
        
        elif privateRoom:
            return PrivateMessage.objects.filter(privateRoom=privateRoom)

        else:
            return PrivateMessage.objects.all()


