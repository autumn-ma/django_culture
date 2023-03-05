from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from djoser import urls as djoser_urls
import social_django.urls as social_urls

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from users.views import social_auth_callback


documentaiton_apis = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

auth_urls = [
    path("", include(djoser_urls)),
    path("social/", include(social_urls, namespace="social")),
    path("social/callback/<str:backend>/", social_auth_callback),
    path("", include("djoser.urls.jwt")),
    path("", include("djoser.urls.authtoken")),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(documentaiton_apis)),
    path("auth/", include(auth_urls)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
