from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.response import Response

from task_manager.models import Task
from task_manager.serializer import UserSerializer, UserLoginSerializer, TaskSerializer


class UserSignUpViewSet(viewsets.ModelViewSet):
    """
    Creates the user
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginViewset(viewsets.ModelViewSet):
    """
    Viewsets for login.Returns token if the user is authenticated
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {}
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                response['token'] = token.key
                response['status'] = 'success'
                response['user_id'] = user.id
                return Response(response, status=HTTP_200_OK)
            response['status'] = 'failed'
            return Response(response, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )


class EmployeeTaskViewset(viewsets.ModelViewSet):
    """
    Viewsets for adding, listing, and editing
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        tasks = Task.objects.filter(employee=self.request.user.id)
        return tasks