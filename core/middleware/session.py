import json
import logging

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger()


class HeadlessSessionCookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith("/auth/_allauth/") and (
            response.status_code == 200
            and hasattr(response, "content")
            and response.get("Content-Type", "").startswith("application/json")
        ):
            try:
                # Parse the response to check for session_token (indicates successful auth)
                response_data = json.loads(response.content)
                if (
                    "meta" in response_data
                    and "session_token" in response_data["meta"]
                    and response_data["meta"]["is_authenticated"]
                ):
                    # Get the user from the response and ensure proper Django login
                    user_id = response_data["data"]["user"]["id"]
                    User = get_user_model()
                    try:
                        user = User.objects.get(id=user_id)

                        # Use Django's login function to ensure proper session setup
                        if not request.user.is_authenticated:
                            login(
                                request,
                                user,
                                backend="django.contrib.auth.backends.ModelBackend",
                            )

                        response.set_cookie(
                            "sessionid",
                            request.session.session_key,
                            max_age=settings.SESSION_COOKIE_AGE,
                            domain=settings.SESSION_COOKIE_DOMAIN,
                            secure=settings.SESSION_COOKIE_SECURE,
                            httponly=settings.SESSION_COOKIE_HTTPONLY,
                            samesite=settings.SESSION_COOKIE_SAMESITE,
                        )

                    except User.DoesNotExist:
                        logger.error(f"User with ID {user_id} not found")

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing response: {e}")

        return response
