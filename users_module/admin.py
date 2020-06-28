from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from users_module.models import User, Daily


# Register your models here.

# Uncomment the following lines to register the custom user model on the Django Admin Panel.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'age', 'gender', 'height', 'weight')}),
        (_('Medical history'), {'fields': (
            'blood_pressure', 'diabetes', 'obesity', 'heart_issues', 'on_immuno_suppressants',
            'kidney_liver_lung_disease',
            'contact_with_positive', 'contact_date', 'quarantine')}),
        (_('COVID Medical Status'), {'fields': ('test_done', 'report_received', 'covid_test_outcome')}),
        (_('Status'), {'fields': ('onboarding_complete',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_filter = ('groups',)
    list_display = ('phone', 'first_name', 'last_name')
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('phone',)


admin.site.register(Daily)
