"""myInstaBase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from storage import views
from storage.views import *
from allauth.socialaccount.providers.vk import views as vk_views

from django.urls import include, re_path


router = routers.DefaultRouter()
router.register(r'api/video', views.VideoViewSet)
router.register(r'api/author', views.AuthorViewSet)
router.register(r'api/comments', views.CommentsViewSet)
router.register(r'api/users', views.UsersViewSet)
router.register(r'api/quotations', views.CommentsQuotationsViewSet)
router.register(r'api/privaterooms', views.PrivateRoomViewSet)
router.register(r'api/prvatemessages', views.PrivateMessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/video/', include('storage.urls')),
    path('api/author/', include('storage.urls')),
    path('api/comments/', include('storage.urls')),
    path('api/users/', include('storage.urls')),
    path('', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('accounts/', IndexView.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/vk/connect', VkConnect.as_view(), name='vk_connect'),
    path('api/auth/vk/login', vk_views.oauth2_login, name='vk_login'),
    path('api/auth/vk/login/callback', vk_callback, name='vk_callback'),
    path('api/auth/vk/login/retrieve/', vk_userDatacallback, name='vk_userDatacallback'),
    path('api/auth/emailverify/', emailverify, name='emailverify'),
    path('api/auth/confimation/', emailconfirm, name='emailconfirm'),
    path('', include('sendOtp.urls')),
    path('send_push/', send_push),
   # path('user/', UserDetailsView.as_view(), name='rest_user_details'),
]


# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)