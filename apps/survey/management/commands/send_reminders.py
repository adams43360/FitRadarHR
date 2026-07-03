"""
send_reminders — relance par email les questionnaires envoyés mais non complétés.

Item #1 de la roadmap V2 (meilleur ratio RICE) : le funnel Analytics montre que
l'essentiel de la déperdition se joue entre l'envoi du lien et le démarrage.
Une relance à J+REMINDER_DELAY_DAYS attaque directement ce point du funnel.

Comportement :
    - Cible les liens au statut PENDING ou IN_PROGRESS, non expirés, envoyés
      depuis au moins REMINDER_DELAY_DAYS jours, jamais relancés.
    - Une seule relance par lien (pas de boucle de spam) — `reminder_sent_at`
      empêche tout renvoi ultérieur.
    - Garde-fou démo : aucun email réel ne part de l'org de démonstration
      (identique aux autres emails du parcours questionnaire).

Usage :
    python manage.py send_reminders            # envoie réellement les emails
    python manage.py send_reminders --dry-run  # liste les liens concernés sans envoyer

Planification (à automatiser côté hébergement, ex. cron système ou service
Docker dédié) :
    0 8 * * * docker compose -f docker/docker-compose.yml exec -T app \\
        python manage.py send_reminders
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.survey.models import QuestionnaireLink
from apps.survey.views import send_reminder_email

REMINDER_DELAY_DAYS = 3


class Command(BaseCommand):
    help = "Envoie une relance email pour les questionnaires envoyés depuis J+3 et non complétés."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Liste les liens qui recevraient une relance, sans envoyer d'email.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        threshold = timezone.now() - timedelta(days=REMINDER_DELAY_DAYS)

        candidates = (
            QuestionnaireLink.objects
            .select_related("person", "org")
            .filter(
                status__in=[
                    QuestionnaireLink.Status.PENDING,
                    QuestionnaireLink.Status.IN_PROGRESS,
                ],
                reminder_sent_at__isnull=True,
                sent_at__lte=threshold,
                expires_at__gt=timezone.now(),
            )
            .exclude(org__is_demo=True)  # garde-fou démo — jamais d'email réel
        )

        sent = 0

        for link in candidates:
            if dry_run:
                self.stdout.write(f"  [dry-run] {link.person.email} ({link.org.name})")
                continue
            send_reminder_email(link)
            sent += 1
            self.stdout.write(f"  Relance envoyée à {link.person.email} ({link.org.name})")

        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f"{candidates.count()} relance(s) seraient envoyée(s)."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(f"{sent} relance(s) envoyée(s)."))
