from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers, exceptions

# Uncomment the following serializers to set up custom serializers for login and registration. You will also have to
# uncomment lines in the settings.py file in order to use custom serializers.
from users_module.models import User, Daily

UserModel = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = None
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = authenticate(self.context['request'], phone=phone, password=password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = None
    phone = PhoneNumberField(required=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'phone': self.validated_data.get('phone', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['phone', 'user_id', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login',
                            'groups', 'user_permissions']


class UserDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    daily_records = UserDailySerializer(many=True)

    class Meta:
        model = User
        exclude = ['password']
