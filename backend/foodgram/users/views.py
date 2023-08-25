# from django.shortcuts import render
from .models import User, Subscribe
from .serializer import (
    UserSerializer,
    ChangePasswordSerializer,
    SubscribeSerializer,
)
from rest_framework import viewsets, generics
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,),
    )
    def selfuser(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def create(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(
                serializer.data.get("current_password")
            ):
                return Response(
                    {"current_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {'message': 'Password updated successfully'},
                status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        queryset = self.request.user.subscribing
        return queryset

    def create(self, request, *args, **kwargs):
        data = {
            'user_id': self.request.user.id,
            'subscribing_user_id': int(kwargs.get('id')),
        }
        serializer = SubscribeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete(self, request, *args, **kwargs):
        Subscribe.objects.filter(
            user_id=self.request.user.id,
            subscribing_user_id=int(kwargs.get('id'))
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
