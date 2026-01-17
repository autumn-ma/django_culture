import datetime
import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.headless.adapter import DefaultHeadlessAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()

logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        logger.info(f"AccountAdapter.save_user called for user: {user.email}")
        user = super().save_user(request, user, form, commit)

        if commit:
            user.save()
        return user

    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)

        invite_code = request.GET.get("invite_code")
        if invite_code:
            logger.info(f"Setting social invite code: {invite_code}")
            request._social_invite_code = invite_code


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        logger.info(
            f"Social login for {sociallogin.account.provider}: {sociallogin.user.email if sociallogin.user else 'No user'}"
        )

        try:
            super().pre_social_login(request, sociallogin)
        except Exception as e:
            logger.error(f"Error in pre_social_login: {str(e)}")
            raise

    def save_user(self, request, sociallogin, form=None):
        logger.info(
            f"SocialAccountAdapter.save_user called for provider: {sociallogin.account.provider}"
        )
        try:
            user = super().save_user(request, sociallogin, form)

            return user
        except Exception as e:
            logger.error(f"Error saving social user: {str(e)}")
            logger.exception("Full traceback:")
            raise

    def authentication_error(
        self,
        request,
        provider_id,
        error=None,
        exception=None,
        extra_context=None,
    ):
        logger.error(
            f"🚨 Authentication error - Provider: {provider_id} (type: {type(provider_id)})"
        )
        logger.error(f"🚨 Error: {error}, Exception: {exception}")

        # Log specific error parameters from Google
        error_params = [
            "error",
            "error_description",
            "error_reason",
            "error_uri",
        ]
        for param in error_params:
            if param in request.GET:
                logger.error(f"🚨 Google sent {param}: {request.GET[param]}")

        try:
            return super().on_authentication_error(
                request, provider_id, error, exception, extra_context
            )
        except Exception as e:
            logger.error(f"🚨 Error in super().authentication_error: {e}")
            raise

    def is_auto_signup_allowed(self, request, sociallogin):
        try:
            result = super().is_auto_signup_allowed(request, sociallogin)
            return result
        except Exception as e:
            logger.error(f"Error in is_auto_signup_allowed: {str(e)}")
            raise

    def populate_user(self, request, sociallogin, data):
        try:
            user = super().populate_user(request, sociallogin, data)
            return user
        except Exception as e:
            logger.error(f"Error in populate_user: {str(e)}")
            raise


class HeadlessAdapter(DefaultHeadlessAdapter):
    pass
