"""
Clés API — item #9 de la roadmap V2 (API publique en lecture seule, US-E1-06).

Une organisation peut générer une ou plusieurs clés API pour connecter un outil
tiers (ATS/SIRH) à FitRadarHR en lecture seule. Chaque clé est scopée à une
seule organisation (isolation multi-tenant stricte, comme le reste du produit).

Sécurité :
  - La valeur en clair de la clé n'est **jamais stockée** — seul un hash SHA-256
    l'est (`key_hash`). Elle n'est affichée qu'une seule fois, au moment de la
    génération (voir `ApiKey.generate`).
  - `key_prefix` (les 12 premiers caractères, non secrets) permet à l'utilisateur
    de reconnaître une clé dans la liste sans avoir à la ré-afficher en entier.
  - Une clé révoquée (`revoked_at` renseigné) n'est plus jamais acceptée par
    `ApiKey.authenticate` — pas de suppression physique, pour garder une trace
    (traçabilité, cohérent avec le reste du produit : journal d'audit immuable).
"""
import hashlib
import secrets
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Organization, User
from core.managers import OrgManager

KEY_PREFIX = "frk_"  # FitRadarHR Key — préfixe visible, pas secret en lui-même


class ApiKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="api_keys",
        verbose_name=_("organisation"),
    )
    name = models.CharField(
        _("nom"), max_length=100,
        help_text=_("Pour vous y retrouver, ex. « Intégration ATS Greenhouse »."),
    )
    key_prefix = models.CharField(_("préfixe"), max_length=12, unique=True)
    key_hash = models.CharField(_("empreinte de la clé"), max_length=64)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_api_keys",
    )
    created_at = models.DateTimeField(_("créée le"), auto_now_add=True)
    last_used_at = models.DateTimeField(_("dernière utilisation"), null=True, blank=True)
    revoked_at = models.DateTimeField(_("révoquée le"), null=True, blank=True)

    objects = OrgManager()

    class Meta:
        verbose_name = _("clé API")
        verbose_name_plural = _("clés API")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.key_prefix}…)"

    @property
    def is_active(self):
        return self.revoked_at is None

    def revoke(self):
        self.revoked_at = timezone.now()
        self.save(update_fields=["revoked_at"])

    @staticmethod
    def _hash(raw_key):
        return hashlib.sha256(raw_key.encode()).hexdigest()

    @classmethod
    def generate(cls, org, name, created_by=None):
        """Crée une nouvelle clé et renvoie `(instance, valeur_en_clair)`.

        La valeur en clair n'est jamais stockée : c'est la seule fois où elle
        est disponible. L'appelant est responsable de l'afficher une fois à
        l'utilisateur (voir la vue de génération)."""
        raw_key = KEY_PREFIX + secrets.token_urlsafe(32)
        instance = cls.objects.create(
            org=org,
            name=name,
            key_prefix=raw_key[:12],
            key_hash=cls._hash(raw_key),
            created_by=created_by,
        )
        return instance, raw_key

    @classmethod
    def authenticate(cls, raw_key):
        """Renvoie la clé API active correspondante, ou `None`."""
        if not raw_key or not raw_key.startswith(KEY_PREFIX):
            return None
        try:
            api_key = cls.objects.select_related("org").get(
                key_hash=cls._hash(raw_key), revoked_at__isnull=True,
            )
        except cls.DoesNotExist:
            return None
        if not api_key.org.is_active:
            return None
        return api_key
