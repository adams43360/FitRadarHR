import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

from core.managers import OrgManager


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
    is_demo = models.BooleanField(
        _("organisation de démonstration"), default=False,
        help_text=_("Org de démo publique — données fictives, emails bloqués, reset périodique."),
    )
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


class OrgSSOConfig(models.Model):
    """Configuration SSO OIDC d'une organisation — item #7 roadmap V2.

    Un IdP (ex. Keycloak) par organisation, jamais partagé entre tenants.
    S'ajoute à la connexion email/mot de passe, ne la remplace jamais (pas de
    verrouillage si l'IdP est indisponible). Synchronisé avec un `SocialApp`
    d'allauth — voir [[apps.accounts.sso]].
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.OneToOneField(
        Organization, on_delete=models.CASCADE,
        related_name="sso_config", verbose_name=_("organisation"),
    )
    enabled = models.BooleanField(_("activé"), default=False)
    display_name = models.CharField(
        _("nom d'affichage"), max_length=100,
        help_text=_("Affiché sur le bouton « Se connecter avec… »."),
    )
    login_slug = models.SlugField(
        _("identifiant de connexion"), max_length=50, unique=True,
        help_text=_("Utilisé dans l'URL de connexion SSO — doit être unique."),
    )
    issuer_url = models.URLField(
        _("URL d'émetteur OIDC"),
        help_text=_("Endpoint de découverte OIDC de votre fournisseur d'identité."),
    )
    client_id = models.CharField(_("client ID"), max_length=255)
    client_secret = models.CharField(
        _("client secret"), max_length=255,
        help_text=_("Jamais ré-affiché après saisie."),
    )
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("configuration SSO")
        verbose_name_plural = _("configurations SSO")

    def __str__(self):
        return f"SSO {self.org} ({self.login_slug})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from .sso import sync_social_app
        sync_social_app(self)

    def delete(self, *args, **kwargs):
        from .sso import delete_social_app
        login_slug = self.login_slug
        super().delete(*args, **kwargs)
        delete_social_app(login_slug)


class Feedback(models.Model):
    """Retour utilisateur in-app — alimente la priorisation de la roadmap.

    Consultable uniquement via l'admin Django (mainteneur du produit) ;
    aucune donnée de personnalité, uniquement le message et la page d'origine.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name="feedbacks", verbose_name=_("organisation"),
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name="feedbacks", verbose_name=_("utilisateur"),
    )
    message = models.TextField(_("message"), max_length=2000)
    page = models.CharField(_("page d'origine"), max_length=255, blank=True)
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)

    objects = OrgManager()

    class Meta:
        verbose_name = _("retour utilisateur")
        verbose_name_plural = _("retours utilisateurs")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback {self.user} — {self.created_at:%d/%m/%Y}"
