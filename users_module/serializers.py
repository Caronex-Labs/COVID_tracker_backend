from django.contrib.auth import get_user_model
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
# Uncomment the following serializers to set up custom serializers for login and registration. You will also have to
# uncomment lines in the settings.py file in order to use custom serializers.
from rest_framework.fields import SerializerMethodField

from users_module.models import User, Daily, Patient

UserModel = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['email', 'user_id', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login',
                            'groups', 'user_permissions', 'is_doctor']


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['patient_id']


class PatientDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        exclude = ['patient']
        read_only_fields = ['date']


class PatientDetailSerializer(serializers.ModelSerializer):
    daily_records = SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['patient_id']

    def get_daily_records(self, instance):
        records = instance.daily_records.all().order_by('-date')
        return PatientDailySerializer(records, many=True).data
