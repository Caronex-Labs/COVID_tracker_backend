# Create your views here.
from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sudarshan_care_backend.permissions import IsOwner
from users_module.models import User, Daily
from users_module.serializers import UserProfileSerializer, UserDailySerializer


class MeFunctionMixin:
    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, IsOwner])
    def profile(self, request):

        serializer = self.get_serializer_class()

        if request.method == 'GET':
            data = serializer(request.user).data
            return Response(data, status=200)

        elif request.method == 'PATCH':
            data = serializer(request.user, request.data, partial=True)
            data.is_valid(raise_exception=True)
            data.save()
        return Response({'message': "User updated"}, status=200)


UserViewSetSerializers = {
    'profile': UserProfileSerializer,
    'daily': UserDailySerializer
}


class UserViewSet(MeFunctionMixin, GenericViewSet):
    lookup_field = 'user_id'
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserViewSetSerializers.get(self.action)

    @action(methods=['get', 'patch'], detail=False)
    def daily(self, request):

        serializer = self.get_serializer_class()

        if request.method == 'GET':
            report = get_object_or_404(Daily, user=request.user, date=date.today())
            data = serializer(report).data
            return Response(data, status=200)

        if request.method == 'PATCH':
            try:
                report = Daily.objects.get_or_create(user=request.user, date=date.today())
                data = serializer(report[0], data=request.data, partial=True)
                data.is_valid(raise_exception=True)
                data.save()
                return Response({"message": "daily report saved"}, status=200)
            except Exception as e:
                print(e)
                return Response({'message': "Error creating daily report"}, status=400)
