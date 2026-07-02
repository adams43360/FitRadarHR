"""
Managers multi-tenant — convention projet (voir CLAUDE.md).

Tout modèle rattaché à une organisation expose `objects.for_org(org)` :
c'est l'unique point d'entrée pour filtrer par tenant. Aucune vue ne doit
refaire un `.filter(org=...)` à la main.
"""
from django.db import models
from django.shortcuts import get_object_or_404


class OrgQuerySet(models.QuerySet):
    """QuerySet des modèles portant une FK directe `org`."""

    org_field = "org"

    def for_org(self, org):
        return self.filter(**{self.org_field: org})


class PersonOrgQuerySet(OrgQuerySet):
    """QuerySet des modèles scopés à l'org via leur FK `person`
    (BigFiveProfile, résultats de fit)."""

    org_field = "person__org"


OrgManager = models.Manager.from_queryset(OrgQuerySet)
PersonOrgManager = models.Manager.from_queryset(PersonOrgQuerySet)


def get_org_object_or_404(model, org, **kwargs):
    """`get_object_or_404` borné au tenant — à utiliser dans toutes les vues."""
    return get_object_or_404(model.objects.for_org(org), **kwargs)
