import json

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.forms import ModelForm, ValidationError
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.models import (
    FeatureFlag,
    FeatureFlagAuditLog,
    FeatureFlagUserOverride,
)
from core.utils.feature_flag import FeatureFlagService

User = get_user_model()


class FeatureFlagAdminForm(ModelForm):
    class Meta:
        model = FeatureFlag
        fields = "__all__"

    def clean_rollout_config(self):
        """Validate rollout configuration based on strategy"""
        rollout_config = self.cleaned_data.get("rollout_config")
        rollout_strategy = self.cleaned_data.get("rollout_strategy")

        if not rollout_config:
            rollout_config = {}

        if rollout_strategy == "user_list":
            if "user_ids" not in rollout_config:
                raise ValidationError(
                    "user_list strategy requires 'user_ids' list in rollout_config"
                )
            if not isinstance(rollout_config["user_ids"], list):
                raise ValidationError("user_ids must be a list")
            # Validate user IDs exist
            user_ids = rollout_config["user_ids"]
            existing_users = User.objects.filter(id__in=user_ids).values_list(
                "id", flat=True
            )
            invalid_ids = set(user_ids) - set(existing_users)
            if invalid_ids:
                raise ValidationError(f"Invalid user IDs: {list(invalid_ids)}")

        elif rollout_strategy == "user_attributes":
            if "conditions" not in rollout_config:
                raise ValidationError(
                    "user_attributes strategy requires 'conditions' list in rollout_config"
                )
            if not isinstance(rollout_config["conditions"], list):
                raise ValidationError("conditions must be a list")
            # Validate condition structure
            for condition in rollout_config["conditions"]:
                if not all(
                    key in condition
                    for key in ["attribute", "operator", "value"]
                ):
                    raise ValidationError(
                        "Each condition must have 'attribute', 'operator', and 'value'"
                    )

        elif rollout_strategy == "gradual":
            required_fields = [
                "start_time",
                "end_time",
                "start_percentage",
                "end_percentage",
            ]
            missing_fields = [
                field
                for field in required_fields
                if field not in rollout_config
            ]
            if missing_fields:
                raise ValidationError(
                    f"gradual strategy requires: {', '.join(missing_fields)}"
                )

        return rollout_config

    def clean(self):
        """Additional validation"""
        cleaned_data = super().clean()
        strategy = cleaned_data.get("rollout_strategy")
        percentage = cleaned_data.get("rollout_percentage")

        if strategy == "percentage" and percentage == 0:
            raise ValidationError(
                "Percentage strategy requires rollout_percentage > 0"
            )

        return cleaned_data


class FeatureFlagUserOverrideInline(admin.TabularInline):
    model = FeatureFlagUserOverride
    extra = 0
    readonly_fields = ["created_at"]
    autocomplete_fields = ["user"]


class FeatureFlagAuditLogInline(admin.TabularInline):
    model = FeatureFlagAuditLog
    extra = 0
    readonly_fields = [
        "timestamp",
        "user",
        "action",
        "old_value",
        "new_value",
        "ip_address",
    ]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    form = FeatureFlagAdminForm
    list_display = [
        "name",
        "is_active",
        "rollout_strategy",
        "rollout_percentage",
        "user_count",
        "created_at",
        "test_flag",
    ]
    list_filter = ["is_active", "rollout_strategy", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at", "flag_status"]
    inlines = [FeatureFlagUserOverrideInline, FeatureFlagAuditLogInline]

    fieldsets = (
        (None, {"fields": ("name", "description", "is_active", "flag_status")}),
        (
            "Rollout Configuration",
            {
                "fields": (
                    "rollout_strategy",
                    "rollout_percentage",
                    "rollout_config",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("user_overrides")

    def user_count(self, obj):
        """Show number of user overrides"""
        count = obj.user_overrides.count()
        if count > 0:
            url = reverse("admin:yourapp_featureflag_change", args=[obj.id])
            return format_html(
                '<a href="{}#featureflag-user-overrides">{} users</a>',
                url,
                count,
            )
        return "0 users"

    user_count.short_description = "Overrides"

    def test_flag(self, obj):
        """Quick test button"""
        return format_html(
            '<button onclick="testFlag(\'{}\')" type="button" class="button">Test</button>',
            obj.name,
        )

    test_flag.short_description = "Test"

    def flag_status(self, obj):
        """Visual status indicator"""
        if obj.is_active:
            color = "green"
            status = "Active"
        else:
            color = "red"
            status = "Inactive"

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status,
        )

    flag_status.short_description = "Status"

    def save_model(self, request, obj, form, change):
        """Override save to add audit logging"""
        old_values = {}
        if change:
            # Get old values for audit
            old_obj = FeatureFlag.objects.get(pk=obj.pk)
            old_values = {
                "is_active": old_obj.is_active,
                "rollout_strategy": old_obj.rollout_strategy,
                "rollout_percentage": old_obj.rollout_percentage,
                "rollout_config": old_obj.rollout_config,
            }

        # Set created_by for new objects
        if not change:
            obj.created_by = request.user

        with transaction.atomic():
            obj.save()

            # Log the action
            FeatureFlagAuditLog.objects.create(
                feature_flag=obj,
                user=request.user,
                action="updated" if change else "created",
                old_value=old_values if change else None,
                new_value={
                    "is_active": obj.is_active,
                    "rollout_strategy": obj.rollout_strategy,
                    "rollout_percentage": obj.rollout_percentage,
                    "rollout_config": obj.rollout_config,
                },
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

            # Invalidate cache
            FeatureFlagService().invalidate_cache(obj.name)

        action = "updated" if change else "created"
        messages.success(
            request, f'Feature flag "{obj.name}" {action} successfully.'
        )

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")

    class Media:
        js = ("admin/js/feature_flag_admin.js",)


@admin.register(FeatureFlagUserOverride)
class FeatureFlagUserOverrideAdmin(admin.ModelAdmin):
    list_display = ["feature_flag", "user", "is_enabled", "created_at"]
    list_filter = ["is_enabled", "created_at", "feature_flag"]
    search_fields = ["feature_flag__name", "user__username", "user__email"]
    autocomplete_fields = ["feature_flag", "user"]
    readonly_fields = ["created_at"]

    def save_model(self, request, obj, form, change):
        """Override save to add audit logging"""
        old_enabled = None
        if change:
            old_obj = FeatureFlagUserOverride.objects.get(pk=obj.pk)
            old_enabled = old_obj.is_enabled

        with transaction.atomic():
            obj.save()

            # Log the action
            FeatureFlagAuditLog.objects.create(
                feature_flag=obj.feature_flag,
                user=request.user,
                action="override_updated" if change else "override_created",
                old_value={"is_enabled": old_enabled} if change else None,
                new_value={
                    "target_user": obj.user.id,
                    "is_enabled": obj.is_enabled,
                },
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

            # Invalidate cache for the specific user
            FeatureFlagService().invalidate_cache(
                obj.feature_flag.name, obj.user.id
            )

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


@admin.register(FeatureFlagAuditLog)
class FeatureFlagAuditLogAdmin(admin.ModelAdmin):
    list_display = [
        "feature_flag",
        "user",
        "action",
        "timestamp",
        "formatted_changes",
    ]
    list_filter = ["action", "timestamp", "feature_flag"]
    search_fields = ["feature_flag__name", "user__username"]
    readonly_fields = [
        "feature_flag",
        "user",
        "action",
        "old_value",
        "new_value",
        "timestamp",
        "ip_address",
        "user_agent",
        "formatted_changes",
    ]
    date_hierarchy = "timestamp"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def formatted_changes(self, obj):
        """Pretty format the changes"""
        if not obj.old_value and not obj.new_value:
            return "No changes"

        changes = []
        if obj.old_value and obj.new_value:
            for key, new_val in obj.new_value.items():
                old_val = obj.old_value.get(key)
                if old_val != new_val:
                    changes.append(f"{key}: {old_val} → {new_val}")
        elif obj.new_value:
            changes.append(f"Created: {obj.new_value}")

        return mark_safe("<br>".join(changes))

    formatted_changes.short_description = "Changes"
