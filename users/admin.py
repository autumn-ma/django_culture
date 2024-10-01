from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date_joined",
        "last_login",
        "is_superuser",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "date_joined",
        "last_login",
        "is_superuser",
        "is_staff",
    )
    raw_id_fields = (
        "groups",
        "user_permissions",
    )
