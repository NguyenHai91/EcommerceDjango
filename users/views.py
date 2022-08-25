
import re
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status

from users.serializers import UserSerializer

User = get_user_model()


# class MyTokenObtainPairView(TokenObtainPairView):
#   serializer_class = MyTokenObtainPairSerializer

class UserView(APIView):
  def post(self, request):
    username = request.data.get('email', '')
    password = request.data.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      refresh = TokenObtainPairSerializer.get_token(user)
      data = {
        'user': str(user),
        'refresh': str(refresh),
        'token': str(refresh.access_token)
      }
      return Response(data, status=status.HTTP_200_OK)
    else:
      return Response({
        'error_message': 'Email or password is incorrect!',
        'error_code': 400
      }, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request):
    if request.user.is_authenticated:
      logout(request)
      print(request.user.is_authenticated)
      return Response(status=status.HTTP_200_OK)
    else:
      return Response(status=status.HTTP_400_BAD_REQUEST)
        

class RegisterView(APIView):
  permission_classes = [AllowAny]

  def post(self, request, *args, **kwargs):
    email = request.data.get("email")
    password = request.data.get("password")
    fullname = request.data.get("fullname")
    phone = request.data.get("phone")
    try:
      user = User.objects.create_user(
        email=email, password=password, full_name=fullname, phone=phone)
      return Response(UserSerializer(user).data)
    except ValueError as err:
      return Response({'error': "Provide Invalid Details"}, status=400)
    except IntegrityError as err:
      return Response({'error': "User Already Exist"}, status=403)


class GetUserView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    return Response(UserSerializer(request.user).data)
