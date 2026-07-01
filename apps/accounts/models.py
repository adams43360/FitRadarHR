import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class Organization(models.Model):
    """Tenant — organisation B2B ou espace personnel B2C."""

    class AccountType(models.TextChoices):
        B2B = "B2B", _("Organisation")
        B2C = "B2C", _("Usage personnel")

    class QuestionnaireVersion(models.TextChoices):
        V50 = "50", _("50 items (~10 min)")
        V100 = "100", _("100 items (~20 min)")

    class Language(models.TextChoices):
        FR = "fr", "Français"
        EN = "en", "English"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("nom"), max_length=255)
    account_type = models.CharField(
        _("type de compte"), max_length=3, choices=AccountType.choices, default=AccountType.B2B
    )
    questionnaire_version = models.CharField(
        _("version du questionnaire"), max_length=3,
        choices=QuestionnaireVersion.choices, default=QuestionnaireVersion.V50
    )
    language_default = models.CharField(
        _("langue par défaut"), max_length=2, choices=Language.choices, default=Language.FR
    )
    is_active = models.BooleanField(_("actif"), default=True)
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("organisation")
        verbose_name_plural = _("organisations")

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("L'email est obligatoire"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Utilisateur ayant un compte FitRadarHR (RH, Manager, ou Solo B2C)."""

    class Role(models.TextChoices):
        RH = "RH", _("Responsable RH")
        MANAGER = "MANAGER", _("Manager")
        SOLO = "SOLO", _("Utilisateur solo")  # B2C — cumule les droits RH + Manager

    class Language(models.TextChoices):
        FR = "fr", "Français"
        EN = "en", "English"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name="users", verbose_name=_("organisation")
    )
    email = models.EmailField(_("email"), unique=True)
    first_name = models.CharField(_("prénom"), max_length=100)
    last_name = models.CharField(_("nom"), max_length=100)
    role = models.CharField(_("rôle"), max_length=10, choices=Role.choices, default=Role.RH)
    language = models.CharField(
        _("langue"), max_length=2, choices=Language.choices, default=Language.FR
    )
    is_active = models.BooleanField(_("actif"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)
    invited_by = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="invitations", verbose_name=_("invité par")
    )
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)
    last_login_at = models.DateTimeField(_("dernière connexion"), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_rh(self):
        return self.role in (self.Role.RH, self.Role.SOLO)

    @property
    def is_manager(self):
        return self.role in (self.Role.MANAGER, self.Role.SOLO)
