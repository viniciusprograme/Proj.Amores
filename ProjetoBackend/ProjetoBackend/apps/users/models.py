from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. A valid email address.')
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text=_('Optional phone number.')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        help_text=_('User profile picture.')
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text=_('Brief user biography.')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} ({self.get_full_name() or self.username})"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else None

    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.is_staff or self.is_superuser

    @property
    def profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [self.first_name, self.last_name, self.phone_number, self.bio, self.avatar]
        completed = sum(1 for field in fields if field)
        return int((completed / len(fields)) * 100)