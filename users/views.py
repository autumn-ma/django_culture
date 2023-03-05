from django.http import JsonResponse
from django.shortcuts import render

from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa


def github_login(request):
    return render(request, "gihub_login.html")


@psa("social:complete")
def social_auth_callback(request, backend):
    user = request.user
    if user.is_authenticated:

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        print("refresh", refresh)
        print("access", access)
        return JsonResponse(
            "refresh: " + str(refresh) + "access: " + str(access), safe=False
        )
