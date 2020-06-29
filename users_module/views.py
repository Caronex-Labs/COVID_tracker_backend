# Create your views here.
from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sudarshan_care_backend.permissions import IsOwner, IsStaff
from users_module.models import User, Daily
from users_module.serializers import UserProfileSerializer, UserDailySerializer, UserDetailSerializer


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

            if (request.user.contact_with_positive or
                    request.user.quarantine or
                    request.user.covid_test_outcome):
                user = User.objects.get(user_id=request.user.user_id)
                user.close_monitoring = True
                user.save()
            else:
                user = User.objects.get(user_id=request.user.user_id)
                user.close_monitoring = False
                user.save()

        return Response({'message': "User updated"}, status=200)


UserViewSetSerializers = {
    'profile': UserProfileSerializer,
    'daily': UserDailySerializer,
    'reports': UserDailySerializer,
    'all': UserProfileSerializer,
    'info': UserDetailSerializer
}


class UserViewSet(MeFunctionMixin, GenericViewSet):
    lookup_field = 'user_id'
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserViewSetSerializers.get(self.action)

    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, IsOwner])
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

                report = report[0]

                if report.dry_cough or report.sore_throat or report.body_ache or report.head_ache or \
                        report.weakness or \
                        report.anosmia or report.ageusia or report.diarrhoea or (
                        report.temperature_evening > 98.5) or (report.temperature_morning > 98.5) or (
                        report.spo2_evening <= 95) or (report.spo2_morning <= 95) or report.difficulty_breathing:
                    user = User.objects.get(user_id=report.user.user_id)
                    user.close_monitoring = True
                    user.save()
                else:
                    user = User.objects.get(user_id=report.user.user_id)
                    user.close_monitoring = False
                    user.save()

                return Response({"message": "daily report saved"}, status=200)
            except Exception as e:
                print(e)
                return Response({'message': "Error creating daily report"}, status=400)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, IsOwner])
    def reports(self, request):
        try:
            reports = Daily.objects.filter(user=request.user)
            serializer = self.get_serializer_class()
            data = serializer(reports, many=True).data
            return Response(data, status=200)
        except Exception as e:
            print(e)
            return Response({"message": "No daily reports found for this user."}, status=404)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, IsStaff])
    def all(self, request):
        serializer = self.get_serializer_class()
        users = User.objects.filter(is_staff=False, is_superuser=False)
        data = serializer(users, many=True).data
        return Response(data, status=200)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated, IsStaff])
    def info(self, request, **kwargs):
        serializer = self.get_serializer_class()
        user = self.get_object()
        data = serializer(user).data
        return Response(data, status=200)
