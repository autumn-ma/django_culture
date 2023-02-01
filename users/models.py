from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=256, default="")
    last_name = models.CharField(max_length=256, default="")
    email = models.CharField(
        _("email"),
        max_length=250,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
