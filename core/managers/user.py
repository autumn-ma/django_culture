from django.contrib.auth.models import UserManager as BaseUserManager

from common.utils.orm import starts_with


class UserManager(BaseUserManager):
    def get_queryset(self):
        qs = super().get_queryset()

        # During migrations, the model might not have these attributes
        # Check if they exist before using them
        if not hasattr(self.model, 'USERNAME_FIELD'):
            return qs

        username_field = self.model.USERNAME_FIELD
        signup_completed_field = self.model.SIGNUP_COMPLETED_FIELD
        unusable_username_prefix = self.model.UNUSABLE_USERNAME_PREFIX
        annotated_qs = qs.annotate(
            **{
                signup_completed_field: starts_with(
                    username_field, unusable_username_prefix
                )
            }
        )
        return annotated_qs
