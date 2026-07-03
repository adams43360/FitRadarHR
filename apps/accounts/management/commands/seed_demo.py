"""
seed_demo — crée (ou réinitialise) l'organisation de démonstration publique.

Contexte fictif : « Nexatech », éditeur de logiciels français d'une centaine
de personnes (équipes dev, produit, sales, finance, RH, customer success).

La commande est idempotente : elle supprime l'org démo existante (cascade)
puis la recrée à l'identique — données déterministes (random seedé).

Usage :
    python manage.py seed_demo            # requiert DEMO_MODE=True
    python manage.py seed_demo --force    # outrepasse le garde-fou DEMO_MODE

Garde-fous liés au mode démo (implémentés dans les vues) :
    - aucun email réel n'est envoyé depuis l'org démo (domaines .example)
    - l'effacement RGPD est désactivé sur l'org démo
    - connexion via le bouton "Essayer la démo" uniquement (mot de passe inutilisable)
"""
import random
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Organization, User
from apps.departments.models import Department
from apps.fit.engine import ALGORITHM_VERSION, compute_all_fits_for_person
from apps.fit.models import BigFiveProfile
from apps.positions.models import Position, PositionProfile
from apps.reports.models import AuditLog
from apps.survey.models import ConsentRecord, QuestionnaireLink
from apps.teams.models import Person, Team, TeamMembership

RNG_SEED = 20260703  # déterministe — chaque reseed produit exactement les mêmes données

# ─── Départements (name_fr, name_en) ─────────────────────────────────────────

DEPARTMENTS = [
    ("Ingénierie", "Engineering"),
    ("Produit & Design", "Product & Design"),
    ("Commercial", "Sales"),
    ("Customer Success", "Customer Success"),
    ("Finance", "Finance"),
    ("Ressources Humaines", "Human Resources"),
]

# ─── Équipes ──────────────────────────────────────────────────────────────────
# archetype : centres OCEAN autour desquels les profils des membres varient (±jitter)
# Les archétypes sont volontairement contrastés pour que les rapports de fit
# et les signaux de complémentarité racontent quelque chose en démo.

TEAMS = [
    {
        "name": "Squad Plateforme",
        "dept": "Ingénierie",
        "desc": "Cœur backend, API et architecture de la plateforme.",
        "archetype": {"O": 62, "C": 78, "E": 38, "A": 60, "N": 34},
        "members": [
            ("Julien", "Moreau"), ("Aïcha", "Benali"), ("Thomas", "Lefèvre"),
            ("Elena", "Petrov"), ("Karim", "Haddad"),
        ],
    },
    {
        "name": "Squad Apps",
        "dept": "Ingénierie",
        "desc": "Applications web et mobile côté client.",
        "archetype": {"O": 70, "C": 64, "E": 50, "A": 62, "N": 38},
        "members": [
            ("Camille", "Roux"), ("Adrien", "Fournier"), ("Lin", "Zhang"),
            ("Sofiane", "Meziane"), ("Margaux", "Perrin"),
        ],
    },
    {
        "name": "Infrastructure & SRE",
        "dept": "Ingénierie",
        "desc": "Infrastructure cloud, fiabilité et outillage interne.",
        "archetype": {"O": 55, "C": 84, "E": 30, "A": 55, "N": 28},
        "members": [
            ("Nicolas", "Girard"), ("Fatou", "Diallo"), ("Maxime", "Bernard"),
            ("Ivan", "Kovac"),
        ],
    },
    {
        "name": "Data",
        "dept": "Ingénierie",
        "desc": "Pipelines de données, analytics et data science.",
        "archetype": {"O": 74, "C": 72, "E": 40, "A": 58, "N": 36},
        "members": [
            ("Louise", "Marchand"), ("Rachid", "El Amrani"), ("Chloé", "Dupont"),
            ("Victor", "Nguyen"),
        ],
    },
    {
        "name": "Produit",
        "dept": "Produit & Design",
        "desc": "Discovery, roadmap et delivery produit.",
        "archetype": {"O": 76, "C": 68, "E": 66, "A": 68, "N": 32},
        "members": [
            ("Damien", "Carvalho"), ("Inès", "Bouzid"), ("Paul", "Renard"),
            ("Anna", "Kowalska"),
        ],
    },
    {
        "name": "Design",
        "dept": "Produit & Design",
        "desc": "Design produit, recherche utilisateur et design system.",
        "archetype": {"O": 84, "C": 58, "E": 56, "A": 70, "N": 42},
        "members": [
            ("Léa", "Vasseur"), ("Hugo", "Blanchard"), ("Sarah", "Cohen"),
        ],
    },
    {
        "name": "Ventes France",
        "dept": "Commercial",
        "desc": "Développement commercial et gestion des comptes France.",
        "archetype": {"O": 58, "C": 62, "E": 82, "A": 60, "N": 30},
        "members": [
            ("Alexandre", "Martin"), ("Nadia", "Cherif"), ("Baptiste", "Leroy"),
            ("Émilie", "Garnier"), ("Yann", "Le Goff"),
        ],
    },
    {
        "name": "Customer Success",
        "dept": "Customer Success",
        "desc": "Accompagnement, adoption et fidélisation des clients.",
        "archetype": {"O": 60, "C": 70, "E": 72, "A": 80, "N": 34},
        "members": [
            ("Manon", "Chevalier"), ("Omar", "Sy"), ("Justine", "Picard"),
            ("David", "Lambert"),
        ],
    },
    {
        "name": "Finance & Admin",
        "dept": "Finance",
        "desc": "Comptabilité, contrôle de gestion et juridique.",
        "archetype": {"O": 44, "C": 86, "E": 36, "A": 58, "N": 36},
        "members": [
            ("Isabelle", "Rousseau"), ("Marc", "Dubois"), ("Amina", "Toure"),
        ],
    },
    {
        "name": "Équipe RH",
        "dept": "Ressources Humaines",
        "desc": "Recrutement, développement des talents et vie d'équipe.",
        "archetype": {"O": 64, "C": 68, "E": 68, "A": 82, "N": 34},
        "members": [
            ("Claire", "Fontaine"), ("Mehdi", "Amrani"), ("Julie", "Berger"),
        ],
    },
]

# ─── Postes ouverts (title_fr, title_en, dept, team, plages OCEAN min/max) ────

POSITIONS = [
    {
        "fr": "Développeur·se Backend Senior", "en": "Senior Backend Developer",
        "dept": "Ingénierie", "team": "Squad Plateforme",
        "desc_fr": "Conception et développement des services cœur de la plateforme (Python, PostgreSQL).",
        "desc_en": "Design and development of core platform services (Python, PostgreSQL).",
        "profile": {"O": (55, 80), "C": (70, 92), "E": (25, 55), "A": (48, 75), "N": (10, 45)},
    },
    {
        "fr": "Ingénieur·e DevOps", "en": "DevOps Engineer",
        "dept": "Ingénierie", "team": "Infrastructure & SRE",
        "desc_fr": "Automatisation de l'infrastructure cloud et fiabilisation des déploiements.",
        "desc_en": "Cloud infrastructure automation and deployment reliability.",
        "profile": {"O": (45, 70), "C": (75, 95), "E": (18, 48), "A": (42, 70), "N": (8, 40)},
    },
    {
        "fr": "Data Engineer", "en": "Data Engineer",
        "dept": "Ingénierie", "team": "Data",
        "desc_fr": "Construction des pipelines de données et industrialisation des modèles.",
        "desc_en": "Building data pipelines and industrializing models.",
        "profile": {"O": (62, 88), "C": (68, 90), "E": (25, 55), "A": (45, 72), "N": (10, 45)},
    },
    {
        "fr": "Product Manager", "en": "Product Manager",
        "dept": "Produit & Design", "team": "Produit",
        "desc_fr": "Discovery, priorisation et delivery sur le périmètre acquisition.",
        "desc_en": "Discovery, prioritization and delivery on the acquisition scope.",
        "profile": {"O": (68, 92), "C": (60, 82), "E": (58, 85), "A": (55, 80), "N": (8, 38)},
    },
    {
        "fr": "Product Designer", "en": "Product Designer",
        "dept": "Produit & Design", "team": "Design",
        "desc_fr": "Design des parcours clés et contribution au design system.",
        "desc_en": "Design of key user journeys and design system contribution.",
        "profile": {"O": (75, 98), "C": (48, 72), "E": (45, 75), "A": (58, 85), "N": (15, 50)},
    },
    {
        "fr": "Account Executive", "en": "Account Executive",
        "dept": "Commercial", "team": "Ventes France",
        "desc_fr": "Cycle de vente complet sur le segment mid-market.",
        "desc_en": "Full sales cycle on the mid-market segment.",
        "profile": {"O": (48, 72), "C": (52, 76), "E": (72, 96), "A": (45, 70), "N": (5, 32)},
    },
    {
        "fr": "Customer Success Manager", "en": "Customer Success Manager",
        "dept": "Customer Success", "team": "Customer Success",
        "desc_fr": "Portefeuille de comptes stratégiques, adoption et renouvellement.",
        "desc_en": "Strategic account portfolio, adoption and renewals.",
        "profile": {"O": (48, 74), "C": (60, 84), "E": (62, 90), "A": (68, 92), "N": (10, 42)},
    },
    {
        "fr": "Comptable Général·e", "en": "General Accountant",
        "dept": "Finance", "team": "Finance & Admin",
        "desc_fr": "Comptabilité générale, clôtures mensuelles et déclarations.",
        "desc_en": "General accounting, monthly closings and filings.",
        "profile": {"O": (32, 58), "C": (78, 98), "E": (25, 55), "A": (48, 75), "N": (12, 48)},
    },
    {
        "fr": "Chargé·e de Recrutement", "en": "Talent Acquisition Specialist",
        "dept": "Ressources Humaines", "team": "Équipe RH",
        "desc_fr": "Recrutement tech et produit, expérience candidat.",
        "desc_en": "Tech and product recruiting, candidate experience.",
        "profile": {"O": (55, 80), "C": (58, 82), "E": (60, 88), "A": (65, 92), "N": (10, 45)},
    },
]

# ─── Candidats externes (prénom, nom, poste ciblé, statut du questionnaire) ──
# "completed" → profil OCEAN calculé (le classement Fit du poste a du contenu)
# "pending" / "in_progress" → alimentent la liste "questionnaires en attente"

CANDIDATES = [
    ("Romain", "Vidal", "Développeur·se Backend Senior", "completed",
     {"O": 68, "C": 74, "E": 42, "A": 63, "N": 30}),
    ("Sonia", "Gharbi", "Développeur·se Backend Senior", "completed",
     {"O": 55, "C": 88, "E": 30, "A": 70, "N": 44}),
    ("Lucas", "Mercier", "Product Manager", "completed",
     {"O": 80, "C": 62, "E": 74, "A": 66, "N": 28}),
    ("Emma", "Silva", "Product Manager", "completed",
     {"O": 58, "C": 82, "E": 48, "A": 55, "N": 52}),
    ("Antoine", "Weber", "Account Executive", "completed",
     {"O": 52, "C": 58, "E": 90, "A": 56, "N": 24}),
    ("Salomé", "Ferrand", "Customer Success Manager", "pending", None),
    ("Mathis", "Aubert", "Data Engineer", "pending", None),
    ("Nora", "Khelifi", "Product Designer", "in_progress", None),
]

DIM_FIELDS = {
    "O": "openness", "C": "conscientiousness", "E": "extraversion",
    "A": "agreeableness", "N": "neuroticism",
}


def _email(first, last, domain):
    slug = f"{first}.{last}".lower()
    for a, b in [("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"),
                 ("â", "a"), ("ï", "i"), ("î", "i"), ("ô", "o"), ("ç", "c"),
                 ("ü", "u"), ("û", "u"), (" ", "-"), ("'", "")]:
        slug = slug.replace(a, b)
    return f"{slug}@{domain}"


class Command(BaseCommand):
    help = "Crée ou réinitialise l'organisation de démonstration (données fictives déterministes)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true",
            help="Exécute même si DEMO_MODE n'est pas activé dans les settings.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEMO_MODE and not options["force"]:
            raise CommandError(
                "DEMO_MODE est désactivé. Activez DEMO_MODE=True dans l'environnement "
                "ou relancez avec --force."
            )

        rng = random.Random(RNG_SEED)
        now = timezone.now()

        # ── Reset : suppression de l'org démo existante (cascade) ──────────
        deleted, _ = Organization.objects.filter(is_demo=True).delete()
        if deleted:
            self.stdout.write(f"Org démo existante supprimée ({deleted} objets).")

        # ── Organisation + comptes ──────────────────────────────────────────
        org = Organization.objects.create(
            name=settings.DEMO_ORG_NAME,
            account_type=Organization.AccountType.B2B,
            is_demo=True,
        )

        def make_user(email, first, last, role):
            user = User(org=org, email=email, first_name=first, last_name=last, role=role)
            user.set_unusable_password()  # connexion uniquement via le bouton démo
            user.save()
            return user

        demo_user = make_user(settings.DEMO_USER_EMAIL, "Alex", "Demo", User.Role.RH)
        manager_eng = make_user(_email("Marie", "Lambert", "nexatech.example"),
                                "Marie", "Lambert", User.Role.MANAGER)
        manager_sales = make_user(_email("Olivier", "Roche", "nexatech.example"),
                                  "Olivier", "Roche", User.Role.MANAGER)

        # ── Départements ────────────────────────────────────────────────────
        departments = {
            fr: Department.objects.create(org=org, name_fr=fr, name_en=en)
            for fr, en in DEPARTMENTS
        }

        # ── Équipes + membres + profils OCEAN ───────────────────────────────
        teams = {}
        persons_with_profile = []
        managers_cycle = {"Ingénierie": manager_eng, "Commercial": manager_sales}

        for spec in TEAMS:
            team = Team.objects.create(
                org=org,
                name=spec["name"],
                description=spec["desc"],
                department=departments[spec["dept"]],
                manager=managers_cycle.get(spec["dept"], demo_user),
            )
            teams[spec["name"]] = team

            for first, last in spec["members"]:
                person = Person.objects.create(
                    org=org,
                    email=_email(first, last, "nexatech.example"),
                    first_name=first,
                    last_name=last,
                    person_type=Person.PersonType.COLLABORATOR,
                    created_by=demo_user,
                )
                TeamMembership.objects.create(team=team, person=person, added_by=demo_user)

                scores = {
                    dim: max(5.0, min(95.0, center + rng.uniform(-14, 14)))
                    for dim, center in spec["archetype"].items()
                }
                self._create_completed_survey(org, person, None, scores, demo_user, rng, now)
                persons_with_profile.append(person)

        # ── Postes + profils cibles ─────────────────────────────────────────
        positions = {}
        for spec in POSITIONS:
            position = Position.objects.create(
                org=org,
                title_fr=spec["fr"],
                title_en=spec["en"],
                description_fr=spec["desc_fr"],
                description_en=spec["desc_en"],
                department=departments[spec["dept"]],
                team=teams[spec["team"]],
                created_by=demo_user,
            )
            profile_kwargs = {}
            for dim, (lo, hi) in spec["profile"].items():
                field = DIM_FIELDS[dim]
                profile_kwargs[f"{field}_min"] = lo
                profile_kwargs[f"{field}_max"] = hi
            PositionProfile.objects.create(position=position, **profile_kwargs)
            positions[spec["fr"]] = position

        # ── Candidats ───────────────────────────────────────────────────────
        for first, last, position_fr, status, scores in CANDIDATES:
            person = Person.objects.create(
                org=org,
                email=_email(first, last, "mail.example"),
                first_name=first,
                last_name=last,
                person_type=Person.PersonType.CANDIDATE,
                created_by=demo_user,
            )
            position = positions[position_fr]
            if status == "completed":
                self._create_completed_survey(org, person, position, scores, demo_user, rng, now)
                persons_with_profile.append(person)
            else:
                link = QuestionnaireLink.objects.create(
                    org=org,
                    person=person,
                    position=position,
                    token=secrets.token_urlsafe(48),
                    questionnaire_version=QuestionnaireLink.Version.V50,
                    language=QuestionnaireLink.Language.FR,
                    sent_by=demo_user,
                    expires_at=now + timedelta(days=7),
                    status=(
                        QuestionnaireLink.Status.IN_PROGRESS
                        if status == "in_progress"
                        else QuestionnaireLink.Status.PENDING
                    ),
                )
                QuestionnaireLink.objects.filter(pk=link.pk).update(
                    sent_at=now - timedelta(days=rng.randint(0, 3))
                )

        # ── Calcul des fits (postes + équipes + complémentarité) ────────────
        for person in persons_with_profile:
            compute_all_fits_for_person(person)

        # ── Un peu d'activité dans le journal d'audit ───────────────────────
        sample_persons = rng.sample(persons_with_profile, 5)
        for i, person in enumerate(sample_persons):
            AuditLog.objects.create(
                org=org,
                user=demo_user,
                action="report.viewed" if i % 2 == 0 else "pdf.exported",
                entity_type="Person",
                entity_id=person.pk,
                metadata={"name": person.full_name},
            )
        AuditLog.objects.create(
            org=org,
            user=None,
            action="demo.reseeded",
            entity_type="Organization",
            entity_id=org.pk,
            metadata={"seed": RNG_SEED},
        )

        self.stdout.write(self.style.SUCCESS(
            f"Org démo « {org.name} » créée : "
            f"{Department.objects.for_org(org).count()} départements, "
            f"{Team.objects.for_org(org).count()} équipes, "
            f"{Position.objects.for_org(org).count()} postes, "
            f"{Person.objects.for_org(org).count()} personnes, "
            f"{BigFiveProfile.objects.for_org(org).count()} profils OCEAN."
        ))

    def _create_completed_survey(self, org, person, position, scores, sent_by, rng, now):
        """Crée un lien complété + consentement + profil Big Five daté dans le passé.

        Les dates sont étalées sur ~5 mois pour que le graphique "profils par mois"
        de la page Analytics raconte une adoption progressive.
        """
        days_ago = rng.randint(2, 150)
        link = QuestionnaireLink.objects.create(
            org=org,
            person=person,
            position=position,
            token=secrets.token_urlsafe(48),
            questionnaire_version=QuestionnaireLink.Version.V50,
            language=QuestionnaireLink.Language.FR,
            sent_by=sent_by,
            expires_at=now - timedelta(days=days_ago) + timedelta(days=7),
            status=QuestionnaireLink.Status.COMPLETED,
            completed_at=now - timedelta(days=days_ago),
        )
        QuestionnaireLink.objects.filter(pk=link.pk).update(
            sent_at=now - timedelta(days=days_ago + rng.randint(1, 4))
        )
        ConsentRecord.objects.create(link=link, language=link.language)
        profile = BigFiveProfile.objects.create(
            person=person,
            link=link,
            openness=round(scores["O"], 2),
            conscientiousness=round(scores["C"], 2),
            extraversion=round(scores["E"], 2),
            agreeableness=round(scores["A"], 2),
            neuroticism=round(scores["N"], 2),
            questionnaire_version=BigFiveProfile.Version.V50,
            algorithm_version=ALGORITHM_VERSION,
        )
        # computed_at est auto_now_add — on l'aligne sur la date de complétion
        BigFiveProfile.objects.filter(pk=profile.pk).update(
            computed_at=now - timedelta(days=days_ago)
        )
