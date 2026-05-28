from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom manager for User model"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a regular user"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    """
    # Remove username field and use email as primary identifier
    username = None

    # Email field (inherited but made required and unique)
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Enter a valid email address.')
    )

    # Additional fields
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
            )
        ],
        help_text=_('Optional. Enter your phone number.')
    )

    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text=_('Optional. Upload a profile picture.')
    )

    bio = models.TextField(
        _('bio'),
        blank=True,
        max_length=500,
        help_text=_('Optional. Tell us about yourself.')
    )

    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True,
        help_text=_('Optional. Your date of birth.')
    )

    # Profile completion tracking
    is_profile_complete = models.BooleanField(
        _('profile complete'),
        default=False,
        help_text=_('Whether the user has completed their profile.')
    )

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Use custom manager
    objects = UserManager()

    # Use email as username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name or self.email.split('@')[0]

    @property
    def profile_completion_percentage(self):
        """
        Calculate profile completion percentage
        """
        fields = [
            self.first_name,
            self.last_name,
            self.phone_number,
            self.bio,
            self.date_of_birth,
            self.avatar
        ]

        completed_fields = sum(1 for field in fields if field)
        total_fields = len(fields)

        percentage = int((completed_fields / total_fields) * 100)

        # Update is_profile_complete if percentage >= 80
        if percentage >= 80 and not self.is_profile_complete:
            self.is_profile_complete = True
            self.save(update_fields=['is_profile_complete'])
        elif percentage < 80 and self.is_profile_complete:
            self.is_profile_complete = False
            self.save(update_fields=['is_profile_complete'])

        return percentage
    """
    Custom user model extending Django's AbstractUser
    """
    # Remove username field and use email as primary identifier
    username = None

    # Email field (inherited but made required and unique)
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Enter a valid email address.')
    )

    # Additional fields
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
            )
        ],
        help_text=_('Optional. Enter your phone number.')
    )

    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text=_('Optional. Upload a profile picture.')
    )

    bio = models.TextField(
        _('bio'),
        blank=True,
        max_length=500,
        help_text=_('Optional. Tell us about yourself.')
    )

    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True,
        help_text=_('Optional. Your date of birth.')
    )

    # Profile completion tracking
    is_profile_complete = models.BooleanField(
        _('profile complete'),
        default=False,
        help_text=_('Whether the user has completed their profile.')
    )

    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Use email as username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name or self.email.split('@')[0]

    @property
    def profile_completion_percentage(self):
        """
        Calculate profile completion percentage
        """
        fields = [
            self.first_name,
            self.last_name,
            self.phone_number,
            self.bio,
            self.date_of_birth,
            self.avatar
        ]

        completed_fields = sum(1 for field in fields if field)
        total_fields = len(fields)

        percentage = int((completed_fields / total_fields) * 100)

        # Update is_profile_complete if percentage >= 80
        if percentage >= 80 and not self.is_profile_complete:
            self.is_profile_complete = True
            self.save(update_fields=['is_profile_complete'])
        elif percentage < 80 and self.is_profile_complete:
            self.is_profile_complete = False
            self.save(update_fields=['is_profile_complete'])

        return percentage