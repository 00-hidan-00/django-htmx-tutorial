from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.conf import settings


class CustomUserManager(UserManager):
    """custom UserManager with unique identifier is email instead of username"""

    def create_user(self, username, email, password=None):
        """Create and return a User with username, email, and password"""

        if email is None:
            raise ValueError("Email is required.")
        if username is None:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        """Create and return a SuperUser with admin permissions."""

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        return user


class User(AbstractUser):
    """User model"""

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Profile model associated to each User object."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.URLField(
        default="https://static.productionready.io/images/smiley-cyrus.jpg"
    )
    bio = models.TextField(max_length=1000, blank=True)
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)


    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Follow `profile`"""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile`"""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Return True if `profile` is in self.follows, False otherwise"""
        return self.follows.filter(pk=profile.pk).exists()
