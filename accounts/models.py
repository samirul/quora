"""
    Made custom user models for user.
"""

import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """UserManager helps to create users with proper validation.

    Args:
        BaseUserManager (Class): Responsible for managing user-related
        models, such as creating user, superusers, custom user objects.
    """
    def create_user(self, username, email, password=None):
        """Create user data.

        Args:
            username (Parameter): Will take username.
            email (Parameter): Will take email.
            password (Parameter, optional): Will take password. Defaults to None.

        Raises:
            ValueError: Validation email error.

        Returns:
            Variable: User.
        """
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self, username, email, password):
        """Create Super user data.

        Args:
            username (Parameter): Will take username.
            email (Parameter): Will take email.
            password (Parameter): Will take password.

        Returns:
            Variable: User.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            
        )
        
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    """Creating custom user model.

    Args:
        AbstractBaseUser (Class): Creating custom user model and adding more
        attribute to the model.

    Returns:
        String: User email.
    """
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=100, unique = True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profilePic = models.ImageField(upload_to='profile-pic', default="/profile-pic/default.png")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """Added custom model name."""
        verbose_name_plural = "User accounts"

    def get_all_permissions(self, user=None):
        """Check for all the permissions in the model.

        Args:
            user (parameter, optional): user information. Defaults to None.

        Returns:
            Returns: If user is admin then return set() or all permissions.
        """
        if user.is_admin:
            return set()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        """Give all permissions to admin only.

        Args:
            perm (Parameter): Get permissions.
            obj (Object, optional): Object. Defaults to None.

        Returns:
            Return: All permissions to the is_admin only.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """It determines whether a user has permissions to view or interact with a specific app.

        Args:
            app_label (String): It determines permissions in the app label(default: Django app names).

        Returns:
            Boolean: Returns True for allowing permission to users.
        """
        return True

    @property
    def is_staff(self):
        """Determines who can login to Django admin panel.

        Returns:
            Returns: Here only admin can login to control panel.
        """
        return self.is_admin