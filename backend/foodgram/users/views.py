from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe, User
from .serializer import (ChangePasswordSerializer, SubscribeSerializer,
                         UserSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return (AllowAny(),)
        else:
            return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('current_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)
                return Response({'message': 'Password changed successfully.'},
                                status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect current password.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = self.request.user.subscribing.all()
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
