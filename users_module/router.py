from rest_framework import routers

from users_module.views import UserViewSet

UserAppRouter = routers.DefaultRouter()

UserAppRouter.register('users', UserViewSet, basename='Users')
