# middleware.py
import json
import logging

from allauth.headless.adapter import get_adapter
from django.http import JsonResponse

logger = logging.getLogger()


class AllAuthConflictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        logger.info(
            f"Middleware - Path: {request.path}, Status: {response.status_code}, User: {request.user.is_authenticated}"
        )

        if (
            response.status_code == 409
            and request.path == "/auth/_allauth/browser/v1/auth/login"
            and request.user.is_authenticated
        ):
            logger.info(
                f"Converting 409 to 200 for authenticated user {request.user}"
            )
            adapter = get_adapter()
            return JsonResponse(
                {
                    "status": 200,
                    "data": {
                        "flows": [],
                        "user": adapter.serialize_user(request.user),
                    },
                }
            )

        return response
