"""
cleanup_e2e_data — supprime les postes créés par les tests E2E Cypress.

Les postes créés par cypress/e2e/creation-poste.cy.js sont préfixés "[E2E]"
dans title_fr (voir testPositionData() dans le spec). Cette commande les
supprime (cascade Django : PositionProfile, PositionFitResult).

Usage :
    python manage.py cleanup_e2e_data              # supprime
    python manage.py cleanup_e2e_data --dry-run     # liste sans supprimer

Appelée automatiquement en fin de run par cypress.config.js (hook after:run),
via `docker compose exec`. Peut aussi être lancée à la main (make cleanup-e2e).
"""
from django.core.management.base import BaseCommand

from apps.positions.models import Position

E2E_TITLE_PREFIX = "[E2E]"


class Command(BaseCommand):
    help = "Supprime les postes créés par les tests E2E Cypress (préfixe [E2E] dans le titre)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Liste les postes qui seraient supprimés, sans les supprimer.",
        )

    def handle(self, *args, **options):
        qs = Position.objects.filter(title_fr__startswith=E2E_TITLE_PREFIX)
        count = qs.count()

        if count == 0:
            self.stdout.write("Aucun poste E2E à supprimer.")
            return

        titles = list(qs.values_list("title_fr", flat=True))

        if options["dry_run"]:
            for title in titles:
                self.stdout.write(f"  - {title}")
            self.stdout.write(self.style.WARNING(f"{count} poste(s) seraient supprimés (dry-run)."))
            return

        qs.delete()
        for title in titles:
            self.stdout.write(f"  - supprimé : {title}")
        self.stdout.write(self.style.SUCCESS(f"{count} poste(s) E2E supprimé(s)."))
