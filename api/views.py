from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.serializers import TaskListSerializer, CustomAuthTokenSerializer, UserDataSerializer
from app.models import Task

User = get_user_model()

''' Custom ObtainAuthToken to get token by confirmed email '''


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name']

    def get_queryset(self):
        username = self.request.user
        return Task.objects.filter(owner=username)

    def perform_create(self, serializer):
        serializer.save(**{'owner': self.request.user})

    '''Action to set important mark'''

    @action(methods=['post'], detail=True)
    def mark_as_important(self, request, pk=None):
        task = self.get_object()
        task.importance = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    ''' Actions to set status'''

    @action(methods=['post'], detail=True)
    def set_status_as_finished(self, request, pk=None):
        task = self.get_object()
        task.set_status_finished()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_todo(self, request, pk=None):
        task = self.get_object()
        task.set_status_todo()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_in_progress(self, request, pk=None):
        task = self.get_object()
        task.set_status_in_progress()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_status_as_blocked(self, request, pk=None):
        task = self.get_object()
        task.set_status_blocked()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    # Actions to set priority
    @action(methods=['post'], detail=True)
    def set_priority_as_low(self, request, pk=None):
        task = self.get_object()
        task.priority = 'low'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_as_medium(self, request, pk=None):
        task = self.get_object()
        task.priority = 'medium'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_priority_as_high(self, request, pk=None):
        task = self.get_object()
        task.priority = 'high'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


''' Permission that user is owner of account '''


class UserIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


''' Get, Put, Patch  methods for User account'''


class UserViewSet(RetrieveModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated, UserIsOwner]

    def get_object(self):
        return self.request.user

