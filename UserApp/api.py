from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

@api_view(['POST'])
def UserCreateApi(request):

    username = request.data['username']
    password = request.data['password']

    User.objects.create_user(username=username, password=password)

    return Response({
        'message': 'User created succesfully'
    })

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protectedView(request):
        return Response({
            'message': 'I am already authenticated',
            'username': request.user.username
        })
    

    

