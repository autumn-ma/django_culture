from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, first name, last name and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        password,
    ):
        """
        Creates and saves a superuser with the given email, first name, last name and password.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user

    def get_by_email(self, email):
        """
        Returns user by email
        """
        return self.get(email=email)
