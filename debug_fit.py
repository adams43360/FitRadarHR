import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.teams.models import Person, Team, TeamMembership
from apps.fit.models import BigFiveProfile, TeamFitResult

# Lister toutes les personnes avec leur profil
print("=== PERSONNES ===")
for p in Person.objects.all().select_related("org"):
    has_profile = hasattr(p, "big_five_profile")
    print(f"  {p.full_name} ({p.email}) — profil: {has_profile}")

print("\n=== ÉQUIPES & MEMBRES ===")
for team in Team.objects.all():
    members = TeamMembership.objects.filter(team=team, left_at__isnull=True).select_related("person")
    print(f"  {team.name}: {[m.person.full_name for m in members]}")

print("\n=== TEAM FIT RESULTS ===")
for r in TeamFitResult.objects.all().select_related("person", "team"):
    print(f"  {r.person.full_name} / {r.team.name} → {r.overall_fit}%")

print("\n=== PERSONNES SANS TEAM FIT ===")
for p in Person.objects.all():
    if not hasattr(p, "big_five_profile"):
        continue
    memberships = TeamMembership.objects.filter(person=p, left_at__isnull=True).select_related("team")
    for m in memberships:
        exists = TeamFitResult.objects.filter(person=p, team=m.team).exists()
        if not exists:
            print(f"  MANQUANT: {p.full_name} / {m.team.name}")
