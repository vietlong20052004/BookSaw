from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    is_staff_user = models.BooleanField("Staff status",
                                        default=False,
                                        help_text="Designates whether the user can manage books and loans.")
    # inherits is_active, is_superuser, etc.

    # override the default groups m2m so it doesn’t clash with auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='accounts_user_set',
        related_query_name='accounts_user',
    )
    # override the default user_permissions m2m similarly
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='accounts_user_permissions',
        related_query_name='accounts_user',
    )