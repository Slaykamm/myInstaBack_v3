from email import message
from http import client
from django.shortcuts import render
from rest_framework.views import APIView
from twilio.rest import Client
import random
from django.http import JsonResponse
from storage.models import Author


class sendOtp(APIView):
    def post(self, request):
        account_sid = 'AC2f76270dd0d3e66fc22fad7250214266'
        auth_token = 'e8320e5c5562464bccfde3ab0d38f8cf'
        number = request.data['number']
        userId = request.data['userId']
        authorId = request.data['authorId']
        # client = Client(account_sid, auth_token)
        otp = generatorOTP()
        body = 'Your confirmation code is: ' + str(otp)
        print(f' SMS: ' + number + ' otp: ' + str(otp) + ' userId: ' + str(userId) + ' authorId: ' + str(authorId))
        confirmPhoneAuthor = Author.objects.get(id=authorId)
        confirmPhoneAuthor.phoneConfirmationCode = otp
        confirmPhoneAuthor.save()

        # message = client.messages.create(from_='+19854653274', body=body, to=str(number))
        # if message.sid:
        print('send succesfull')
        return JsonResponse({'success': True})
        # else:
        #     print('send failed')
        #     return JsonResponse({'success': False})

def generatorOTP():
    return random.randint(100000, 999999)