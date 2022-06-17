from dataclasses import field
from rest_framework import serializers
from storage.models import Video, Author, Comments, User, CommentsQuotations, PrivateRoom, PrivateMessage


from django.conf import settings



#--------------AUTHOR
class AuthorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



# костылим 

class AuthorViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'




#--------------VIDEO
class VideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'



# костылим 

class VideoViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'

#--------------Comments

class CommentsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'



# костылим 

class CommentsViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'


#--------------USER

class UsersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



# костылим 

class UsersViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


#--------------CommentsQuotations

class CommentsQuotationsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsQuotations
        fields = '__all__'



# костылим 

class CommentsQuotationsViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentsQuotations
        fields = '__all__'


#----------------PrivateRooms

class PrivateRoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateRoom
        fields = '__all__'



# костылим 

class PrivateRoomViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivateRoom
        fields = '__all__'


#----------------PrivateMessages

class PrivateMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = '__all__'



# костылим 

class PrivateMessageViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivateMessage
        fields = '__all__'


from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)




class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    @staticmethod
    def validate_username(username):
        print('username', username)
        if 'allauth.account' not in settings.INSTALLED_APPS:
            # We don't need to call the all-auth
            # username validator unless its installed
            return username

        from allauth.account.adapter import get_adapter
        username = get_adapter().clean_username(username)
        return username

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(User, 'USERNAME_FIELD'):
            extra_fields.append(User.USERNAME_FIELD)
        if hasattr(User, 'EMAIL_FIELD'):
            extra_fields.append(User.EMAIL_FIELD)
        if hasattr(User, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(User, 'last_name'):
            extra_fields.append('last_name')
        model = User
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)
