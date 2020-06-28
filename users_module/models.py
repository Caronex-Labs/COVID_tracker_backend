from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
#
# Uncomment and edit the following User model and the Custom UserManager to represent your needs. The following has
# been coded to use Email instead of username, feel free to modify it for any particular use-case you need it for.
# You must also uncomment a line in the settings.py file that sets this model as the Auth User Model
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = None
    user_id = models.AutoField(primary_key=True)
    phone = PhoneNumberField(unique=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, choices=(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Rather not say', 'Rather not say'),
    ), null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    blood_pressure = models.BooleanField(default=False, null=True)
    diabetes = models.BooleanField(default=False, null=True)
    obesity = models.BooleanField(default=False, null=True)
    heart_issues = models.BooleanField(default=False, null=True)
    on_immuno_suppressants = models.BooleanField(default=False, null=True)
    kidney_liver_lung_disease = models.BooleanField(default=False, null=True)
    contact_with_positive = models.BooleanField(default=False, null=True)
    contact_date = models.DateField(blank=True, null=True)
    quarantine = models.BooleanField(default=False, null=True)
    onboarding_complete = models.BooleanField(default=False, null=True)
    test_done = models.BooleanField(default=False)
    report_received = models.BooleanField(default=False)
    covid_test_outcome = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def is_owner(self, user):
        return self.phone == user.phone


class Daily(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_records')
    date = models.DateField()

    dry_cough = models.BooleanField(default=False)
    dry_cough_frequency = models.IntegerField(blank=True, null=True)
    sore_throat = models.BooleanField(default=False)
    body_ache = models.BooleanField(default=False)
    body_ache_intensity = models.IntegerField(blank=True, null=True)
    head_ache = models.BooleanField(default=False)
    head_ache_intensity = models.IntegerField(blank=True, null=True)
    weakness = models.BooleanField(default=False)
    anosmia = models.BooleanField(default=False)
    ageusia = models.BooleanField(default=False)
    diarrhoea = models.BooleanField(default=False)
    diarrhoea_frequency = models.IntegerField(blank=True, null=True)
    temperature_morning = models.IntegerField(blank=True, null=True)
    temperature_evening = models.IntegerField(blank=True, null=True)
    spo2 = models.IntegerField(blank=True, null=True)
    appetite_level = models.IntegerField(blank=True, null=True)
    abnormal_medical_reports = models.BooleanField(default=False)
    report = models.URLField(blank=True, null=True)
    difficulty_breathing = models.BooleanField(default=False)
