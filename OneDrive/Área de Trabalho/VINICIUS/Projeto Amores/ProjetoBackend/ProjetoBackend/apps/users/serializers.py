from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_completion = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'avatar', 'bio', 'is_active', 'date_joined',
            'updated_at', 'password', 'password_confirm', 'full_name',
            'profile_completion'
        ]
        read_only_fields = ['id', 'date_joined', 'updated_at', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_profile_completion(self, obj):
        return obj.profile_completion_percentage

    def validate(self, attrs):
        """Validate password confirmation and other fields"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': _("Password confirmation doesn't match.")
            })

        # Remove password_confirm from validated data
        attrs.pop('password_confirm', None)
        return attrs

    def create(self, validated_data):
        """Create user with hashed password"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update user with password handling"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile operations (read/update)"""

    full_name = serializers.SerializerMethodField(read_only=True)
    profile_completion = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'avatar', 'bio', 'date_joined',
            'updated_at', 'full_name', 'profile_completion'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_profile_completion(self, obj):
        return obj.profile_completion_percentage


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,  # Django authenticate uses username field
                password=password
            )

            if not user:
                raise serializers.ValidationError({
                    'non_field_errors': [_('Invalid email or password.')]
                })

            if not user.is_active:
                raise serializers.ValidationError({
                    'non_field_errors': [_('User account is disabled.')]
                })

            attrs['user'] = user
        else:
            raise serializers.ValidationError({
                'non_field_errors': [_('Must include email and password.')]
            })

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        # Check old password
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({
                'old_password': _('Current password is incorrect.')
            })

        # Check password confirmation
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': _("Password confirmation doesn't match.")
            })

        # Check if new password is different from old
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({
                'new_password': _('New password must be different from current password.')
            })

        return attrs