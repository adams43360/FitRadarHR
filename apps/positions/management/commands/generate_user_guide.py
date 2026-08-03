"""
generate_user_guide — assemble les captures Cypress en un guide PDF utilisateur.

S'appuie sur les captures produites par cypress/e2e/creation-poste.cy.js (voir
cypress/screenshots/creation-poste.cy.js/<lang>/*.png — un sous-dossier par
langue, cf. cy.maybeScreenshot() dans cypress/support/commands.js) et un petit
manifeste de texte FR/EN ci-dessous pour générer un PDF aux couleurs de
FitRadarHR, via le même mécanisme que les exports de rapports (WeasyPrint,
template CSS-only — voir apps/reports/views.py::_render_pdf).

À lancer à chaque évolution du parcours de création de poste (nouveau champ,
étape modifiée, etc.) : le manifeste ci-dessous doit alors être mis à jour à la
main (le texte n'est pas déductible des captures).

Usage :
    python manage.py generate_user_guide                 # régénère FR + EN
    python manage.py generate_user_guide --lang fr        # une seule langue
    make generate-doc                                     # relance Cypress (FR puis EN) puis cette commande

Prérequis : les captures des deux langues doivent exister — lancer
`npm run test:e2e` (français) et `npm run test:e2e:en` (anglais, bascule la
langue via le vrai sélecteur de l'app) avant si besoin.
"""
import base64

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import translation

SCREENSHOTS_BASE_DIR = settings.BASE_DIR / "cypress" / "screenshots" / "creation-poste.cy.js"
OUTPUT_DIR = settings.BASE_DIR / "docs" / "user" / "assets"

GUIDE_TITLE = {
    "fr": "Créer un poste et définir son profil Big Five cible",
    "en": "Creating a position and defining its target Big Five profile",
}

GUIDE_INTRO = {
    "fr": (
        "Ce guide illustre, étape par étape, la création d'un poste et la "
        "définition de son profil Big Five cible dans FitRadarHR. Généré "
        "automatiquement à partir du test end-to-end Cypress qui reproduit ce "
        "parcours — rappel : le profil cible informe une décision humaine, il "
        "ne la remplace jamais."
    ),
    "en": (
        "This guide walks through, step by step, creating a position and "
        "defining its target Big Five profile in FitRadarHR. Automatically "
        "generated from the Cypress end-to-end test that reproduces this flow "
        "— reminder: the target profile informs a human decision, it never "
        "replaces one."
    ),
}

# Manifeste texte par capture — à mettre à jour à la main si le parcours change
# (nouvelle étape, champ renommé, capture renommée dans le spec Cypress...).
STEPS = [
    {
        "screenshot": "01-etape1-connexion-dashboard.png",
        "title": {"fr": "Se connecter", "en": "Log in"},
        "body": {
            "fr": (
                "Connectez-vous avec vos identifiants pour accéder au tableau de "
                "bord de votre organisation. Cet écran donne une vue d'ensemble : "
                "nombre de postes actifs, équipes, personnes suivies, et "
                "questionnaires en attente."
            ),
            "en": (
                "Log in with your credentials to access your organization's "
                "dashboard. This screen gives an overview: number of active "
                "positions, teams, tracked people, and pending questionnaires."
            ),
        },
    },
    {
        "screenshot": "02-etape2-formulaire-nouveau-poste.png",
        "title": {"fr": "Créer un nouveau poste", "en": "Create a new position"},
        "body": {
            "fr": (
                "Depuis le tableau de bord ou le menu Recrutement > Postes, "
                "cliquez sur « + Nouveau poste » pour ouvrir le formulaire de "
                "création. Seul le titre en français est obligatoire ; le reste "
                "(titre anglais, département, équipe cible, description) est "
                "optionnel et pourra être complété plus tard."
            ),
            "en": (
                "From the dashboard or the Recruitment > Positions menu, click "
                "“+ New position” to open the creation form. Only the French "
                "title is required; everything else (English title, department, "
                "target team, description) is optional and can be filled in "
                "later."
            ),
        },
    },
    {
        "screenshot": "03-etape3a-formulaire-poste-rempli.png",
        "title": {"fr": "Renseigner le formulaire", "en": "Fill in the form"},
        "body": {
            "fr": (
                "Renseignez le titre du poste en français et, idéalement, sa "
                "traduction anglaise dès la création : cela facilite l'envoi du "
                "questionnaire à des candidats internationaux, qui recevront le "
                "lien dans leur langue. Vous pouvez aussi rattacher le poste à "
                "un département existant, une équipe cible pour comparer le "
                "fit, et ajouter une description du contexte et des missions "
                "principales."
            ),
            "en": (
                "Enter the position title in French and, ideally, its English "
                "translation right from creation: this makes it easier to send "
                "the questionnaire to international candidates, who will "
                "receive the link in their own language. You can also attach "
                "the position to an existing department, a target team to "
                "compare fit against, and add a description of the context and "
                "main responsibilities."
            ),
        },
    },
    {
        "screenshot": "04-etape3b-poste-cree-arrivee-profil-big-five.png",
        "title": {"fr": "Poste créé", "en": "Position created"},
        "body": {
            "fr": (
                "Le poste est créé avec le statut Actif, mais sans profil Big "
                "Five pour l'instant. Vous êtes automatiquement redirigé vers "
                "l'écran de définition du profil cible — l'étape suivante "
                "indispensable pour que le moteur de Fit puisse comparer des "
                "personnes à ce poste."
            ),
            "en": (
                "The position is created with Active status, but without a Big "
                "Five profile yet. You're automatically redirected to the "
                "target profile screen — the next essential step so the Fit "
                "engine can compare people against this position."
            ),
        },
    },
    {
        "screenshot": "05-etape4a-profil-big-five-rempli.png",
        "title": {"fr": "Définir le profil Big Five cible", "en": "Define the target Big Five profile"},
        "body": {
            "fr": (
                "Pour chacune des cinq dimensions du modèle Big Five / OCEAN "
                "(Ouverture, Conscience, Extraversion, Agréabilité, Stabilité "
                "émotionnelle), ajustez les curseurs Min et Max pour définir la "
                "fourchette de score (0 à 100) jugée adaptée au poste. Survolez "
                "le nom d'une dimension pour afficher une infobulle expliquant "
                "ce que signifie un score élevé ou faible, directement dans "
                "l'interface."
            ),
            "en": (
                "For each of the five Big Five / OCEAN dimensions (Openness, "
                "Conscientiousness, Extraversion, Agreeableness, Emotional "
                "stability), adjust the Min and Max sliders to define the score "
                "range (0 to 100) considered suitable for the position. Hover "
                "over a dimension's name to see a tooltip explaining what a "
                "high or low score means, right in the interface."
            ),
        },
    },
    {
        "screenshot": "06-etape4b-profil-enregistre-detail-poste.png",
        "title": {"fr": "Profil enregistré", "en": "Profile saved"},
        "body": {
            "fr": (
                "Une fois enregistré, le profil cible est immédiatement "
                "disponible pour le calcul de fit : la fiche du poste affiche "
                "désormais les fourchettes définies pour chaque dimension, "
                "ainsi qu'un classement des personnes déjà évaluées, filtrable "
                "entre candidats et collaborateurs."
            ),
            "en": (
                "Once saved, the target profile is immediately available for "
                "fit calculations: the position page now shows the defined "
                "ranges for each dimension, along with a ranking of "
                "already-assessed people, filterable between candidates and "
                "collaborators."
            ),
        },
    },
    {
        "screenshot": "07-etape5-poste-present-dans-la-liste.png",
        "title": {"fr": "Retrouver le poste dans la liste", "en": "Find the position in the list"},
        "body": {
            "fr": (
                "Le nouveau poste apparaît désormais dans la liste accessible "
                "depuis le menu Recrutement > Postes, avec le badge « Profil "
                "configuré » qui confirme qu'un profil Big Five cible a bien "
                "été défini. Un filtre permet de basculer entre postes actifs "
                "et archivés."
            ),
            "en": (
                "The new position now appears in the list under the "
                "Recruitment > Positions menu, with the “Profile configured” "
                "badge confirming a target Big Five profile has been set. A "
                "filter lets you switch between active and archived positions."
            ),
        },
    },
    {
        "screenshot": "08-etape6-detail-poste-verification-finale.png",
        "title": {"fr": "Vérifier le détail du poste", "en": "Review the position details"},
        "body": {
            "fr": (
                "En cliquant sur « Voir » depuis la liste, vous retrouvez la "
                "fiche complète du poste : titre (FR/EN), description, "
                "département et équipe éventuellement rattachés, et le profil "
                "Big Five cible tel que configuré à l'étape précédente. C'est "
                "aussi depuis cette fiche que le poste pourra être modifié ou "
                "archivé plus tard."
            ),
            "en": (
                "Clicking “View” from the list opens the position's full page: "
                "title (FR/EN), description, any attached department and team, "
                "and the target Big Five profile as configured in the previous "
                "step. This page is also where the position can later be "
                "edited or archived."
            ),
        },
    },
]


class Command(BaseCommand):
    help = "Génère le guide PDF utilisateur (FR/EN) à partir des captures Cypress du parcours de création de poste."

    def add_arguments(self, parser):
        parser.add_argument(
            "--lang",
            choices=["fr", "en"],
            help="Ne générer qu'une langue (par défaut : les deux).",
        )

    def handle(self, *args, **options):
        languages = [options["lang"]] if options["lang"] else ["fr", "en"]

        for lang in languages:
            screenshots_dir = SCREENSHOTS_BASE_DIR / lang
            if not screenshots_dir.exists():
                run_cmd = "npm run test:e2e" if lang == "fr" else "npm run test:e2e:en"
                raise CommandError(
                    f"Dossier de captures introuvable : {screenshots_dir}\n"
                    f"Lancer d'abord `{run_cmd}` (depuis la racine du projet, "
                    "hors conteneur) pour générer les captures Cypress en "
                    f"{lang}."
                )

            missing = [
                step["screenshot"] for step in STEPS
                if not (screenshots_dir / step["screenshot"]).exists()
            ]
            if missing:
                raise CommandError(
                    f"Capture(s) manquante(s) dans {screenshots_dir} : "
                    f"{', '.join(missing)}\n"
                    "Le manifeste STEPS (dans cette commande) ne correspond peut-être "
                    "plus aux noms de cy.maybeScreenshot() du spec — vérifier "
                    "cypress/e2e/creation-poste.cy.js."
                )

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        for lang in languages:
            self._generate_pdf(lang)

    def _generate_pdf(self, lang):
        from weasyprint import HTML

        screenshots_dir = SCREENSHOTS_BASE_DIR / lang
        steps_context = []
        for step in STEPS:
            image_path = screenshots_dir / step["screenshot"]
            encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
            steps_context.append({
                "title": step["title"][lang],
                "body": step["body"][lang],
                "image_data_uri": f"data:image/png;base64,{encoded}",
            })

        with translation.override(lang):
            html_string = render_to_string("docs/pdf/user_guide.html", {
                "lang": lang,
                "guide_title": GUIDE_TITLE[lang],
                "guide_intro": GUIDE_INTRO[lang],
                "steps": steps_context,
            })

        pdf_bytes = HTML(string=html_string).write_pdf()
        output_path = OUTPUT_DIR / f"guide-creation-poste-{lang}.pdf"
        output_path.write_bytes(pdf_bytes)
        self.stdout.write(self.style.SUCCESS(f"PDF généré : {output_path}"))
