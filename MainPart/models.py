from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.contrib.auth.models import User, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator


class Role(models.Model):
    role_name = models.CharField(max_length=20)

    def __str__(self):
        return self.role_name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, surname, username, password, **extra_fields):
        """
        FUnction to create our user, bcs we change basic user model,
        to custom. As arguments we have a REQUIRED FIELDS in our model
        extra fields are fields those exist in User model, and
        using these we can make a superuser and working in login etc
        """

        if not email:
            raise ValueError("Email is none")
        if not first_name:
            raise ValueError("Nme is empty")
        if not surname:
            raise ValueError("Surname is empty")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            surname=surname,
            username=username,
            **extra_fields
        )
        user.set_password(password)     # used to set a password to our user
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, surname, username, password, **extra_fields):
        """
        Create and save an Super User with the given EMAIL, FIRST_NAME, LAST_NAME and Password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            surname=surname,
            password=password,
            username=username
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=40, blank=True)
    surname = models.CharField(_('last name'), max_length=50, blank=True, default="")
    data_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    password = models.CharField(_('password'), max_length=60, blank=False)

    is_active = models.BooleanField(_('is_active'), default=True)
    is_superuser = models.BooleanField(_('is_superuser'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=True)
    is_admin = models.BooleanField(_('is_admin'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @staticmethod
    def existance(self, username):
        try:
            exist = CustomUser.objects.all().get(email=username)
        except ValueError:
            raise ValueError("This value exist in database")
        return True


class CustomerCard(models.Model):
    card_number = models.IntegerField()
    safe_code = models.IntegerField(
        validators=[
            MaxValueValidator(999),
            MinValueValidator(000),

        ]
    )
    user_connect = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_connect

    @classmethod
    def _len_validator(cls) -> bool:
        value_length = str(cls.safe_code)
        if len(value_length) > 3 or len(value_length) < 3:
            return False
        return True

    @staticmethod
    def static_method():
        print("esa")



