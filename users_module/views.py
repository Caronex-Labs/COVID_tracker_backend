# Create your views here.
from datetime import date

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sudarshan_care_backend.permissions import IsOwner, IsStaff
from users_module.models import User, Patient, Daily
from users_module.serializers import PatientProfileSerializer, \
    PatientDetailSerializer, UserProfileSerializer, PatientDailySerializer


class MeFunctionMixin:
    """
    A mixin to provide the current users profile.
    """

    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, IsOwner])
    def profile(self, request):

        serializer = self.get_serializer_class()

        if request.method == 'GET':
            data = serializer(request.user).data
            return Response(data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            data = serializer(request.user, request.data, partial=True)
            data.is_valid(raise_exception=True)
            data.save()

        return Response({'message': "User updated"}, status=status.HTTP_200_OK)


class UserViewSet(MeFunctionMixin, GenericViewSet):
    """
    Contains endpoints pertaining to the current user.
    """
    lookup_field = 'user_id'
    permission_classes = [IsAuthenticated]
    UserViewSetSerializers = {
        'profile': UserProfileSerializer,
    }

    queryset = User.objects.all()

    def get_serializer_class(self):
        return self.UserViewSetSerializers.get(self.action)


class PatientViewSet(GenericViewSet):
    """
    Contains endpoints pertaining to the patients
    """
    lookup_field = 'patient_id'
    permission_classes = [IsAuthenticated, IsStaff]
    PatientViewSetSerializers = {
        'all': PatientProfileSerializer,
        'info': PatientDetailSerializer,
        'add': PatientProfileSerializer,
        'daily': PatientDailySerializer
    }

    queryset = Patient.objects.all()

    def get_serializer_class(self):
        return self.PatientViewSetSerializers.get(self.action)

    @action(methods=['get'], detail=False)
    def all(self, request):
        serializer = self.get_serializer_class()
        patients = Patient.objects.filter()
        serializer_data = serializer(patients, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)

    @action(methods=['get', 'patch'], detail=True)
    def info(self, request, **kwargs):
        if request.method == 'GET':
            serializer = self.get_serializer_class()
            user = self.get_object()
            serializer_data = serializer(user).data
            return Response(serializer_data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = self.get_serializer_class()
            patient = self.get_object()
            data = serializer(patient, request.data, partial=True)
            data.is_valid(raise_exception=True)
            data.save()
            return Response({'message': "Patient updated"}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def add(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        patient = serializer_data.save()

        if ((patient.contact_with_positive or
             patient.quarantine or
             patient.covid_test_outcome) and not patient.hospitalized):
            patient = Patient.objects.get(patient_id=patient.patient_id)
            patient.close_monitoring = True
            patient.save()
        else:
            user = User.objects.get(user_id=request.user.user_id)
            user.close_monitoring = False
            user.save()

        return Response({"message": "Patient record created", "patient_id": patient.patient_id},
                        status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=True)
    def daily(self, request, **kwargs):
        try:
            report = Daily.objects.get_or_create(patient=Patient.objects.get(patient_id=kwargs['patient_id']),
                                                 date=date.today())
            serializer = self.get_serializer_class()
            data = serializer(report[0], data=request.data, partial=True)
            data.is_valid(raise_exception=True)
            data.save()

            report = report[0]

            if report.dry_cough or report.sore_throat or report.body_ache or report.head_ache or \
                    report.weakness or \
                    report.anosmia or report.ageusia or report.diarrhoea or (
                    report.temperature_evening > 98.5) or (report.temperature_morning > 98.5) or (
                    report.spo2_evening <= 95) or (report.spo2_morning <= 95) or report.difficulty_breathing:
                patient = Patient.objects.get(patient_id=report.patient.patient_id)
                patient.close_monitoring = True
                patient.save()
            else:
                user = User.objects.get(user_id=report.user.user_id)
                user.close_monitoring = False
                user.save()

            return Response({"message": "daily report saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': "Error creating daily report"}, status=status.HTTP_400_BAD_REQUEST)
