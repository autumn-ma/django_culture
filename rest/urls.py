from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

# from rest.v0.views import
#     LoginView,
#     LogoutView,
# )

urlpatterns = [
    # auth urls
    # path("auth/login/", LoginView.as_view(), name="login"),
    # path("auth/logout/", LogoutView.as_view(), name="logout"),
]

router = DefaultRouter()

# router.register("auth/users", UserViewSet, basename="users")

urlpatterns += router.urls
