from rest_framework import routers

from users_module.views import UserViewSet, PatientViewSet

UserAppRouter = routers.DefaultRouter()

UserAppRouter.register('users', UserViewSet, basename='Users')
UserAppRouter.register('patients', PatientViewSet, basename='Patients')
