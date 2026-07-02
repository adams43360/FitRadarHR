"""Helpers partagés pour les tests."""
from apps.accounts.models import Organization, User


def create_org_and_user(name="Org Test", email="user@example.com", role=None):
    """Crée une organisation B2B et un utilisateur rattaché."""
    org = Organization.objects.create(name=name)
    user = User.objects.create_user(
        email=email,
        password="test-password",
        first_name="Test",
        last_name="User",
        org=org,
        role=role or User.Role.RH,
    )
    return org, user


def create_profile(person, o=50, c=50, e=50, a=50, n=50):
    """Crée un BigFiveProfile avec des scores donnés."""
    from apps.fit.models import BigFiveProfile

    return BigFiveProfile.objects.create(
        person=person,
        openness=o,
        conscientiousness=c,
        extraversion=e,
        agreeableness=a,
        neuroticism=n,
        questionnaire_version="50",
    )
