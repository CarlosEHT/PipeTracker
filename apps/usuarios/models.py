from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from apps.core import models as core_models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")

        required_fields = ["nombre", "apellido_p"]
        for field in required_fields:
            if not extra_fields.get(field):
                raise ValueError(f"El campo {field} es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, db_column="id")

    nombre = models.CharField(
        max_length=50,
        verbose_name="nombre"
    )
    apellido_p = models.CharField(
        max_length=100,
        verbose_name="apellido paterno"
    )
    apellido_m = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="apellido materno"
    )
    telefono = models.CharField(
        max_length=20,
        verbose_name="teléfono"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="correo electrónico"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="usuario activo"
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="es staff"
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="es superusuario"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de registro"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido_p"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return " ".join(filter(None, [
            self.nombre,
            self.apellido_p,
            self.apellido_m
        ]))


    def get_short_name(self):
        return self.nombre
