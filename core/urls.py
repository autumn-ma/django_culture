from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from djoser import urls as djoser_urls

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

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
    path("", include("djoser.urls.jwt")),
    path("", include("djoser.urls.authtoken")),
]

api_v1_urls = []

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(documentaiton_apis)),
    path("auth/", include(auth_urls)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
