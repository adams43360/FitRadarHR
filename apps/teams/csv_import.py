"""Import en masse de personnes (candidats/collaborateurs) via CSV.

Colonnes attendues (en-tête, insensible à la casse) : first_name, last_name,
email, person_type (optionnel — "candidate"/"candidat" ou
"collaborator"/"collaborateur", "candidate" par défaut).
"""
import csv
import io

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext as _

from .models import Person

REQUIRED_HEADERS = {"first_name", "last_name", "email"}

PERSON_TYPE_ALIASES = {
    "candidate": Person.PersonType.CANDIDATE,
    "candidat": Person.PersonType.CANDIDATE,
    "candidate(e)": Person.PersonType.CANDIDATE,
    "collaborator": Person.PersonType.COLLABORATOR,
    "collaborateur": Person.PersonType.COLLABORATOR,
    "collaborateur(rice)": Person.PersonType.COLLABORATOR,
    "collaboratrice": Person.PersonType.COLLABORATOR,
}


class CSVImportError(Exception):
    """Erreur bloquante (en-têtes manquants, fichier illisible…)."""


def _normalize_person_type(raw):
    key = (raw or "").strip().lower()
    return PERSON_TYPE_ALIASES.get(key, Person.PersonType.CANDIDATE)


def import_persons_csv(uploaded_file, org, user, max_new=None):
    """Parse et importe un fichier CSV de personnes pour `org`.

    `max_new` (optionnel) plafonne le nombre de personnes réellement créées —
    utilisé pour respecter le quota du plan gratuit (roadmap V3 #2) : les
    lignes excédentaires sont comptées dans `skipped_quota` plutôt que rejetées
    silencieusement ou en erreur.

    Renvoie {"created": int, "skipped_existing": int, "skipped_quota": int,
    "row_errors": [(line, message), ...]}.
    Lève CSVImportError si le fichier est illisible ou si les colonnes obligatoires manquent.
    """
    try:
        raw = uploaded_file.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        raise CSVImportError(_("Le fichier n'est pas un CSV valide (encodage non reconnu)."))

    reader = csv.DictReader(io.StringIO(raw))
    if not reader.fieldnames:
        raise CSVImportError(_("Le fichier est vide."))

    headers = {h.strip().lower() for h in reader.fieldnames if h}
    missing = REQUIRED_HEADERS - headers
    if missing:
        raise CSVImportError(
            _("Colonnes manquantes dans le CSV : %(cols)s") % {"cols": ", ".join(sorted(missing))}
        )

    # Table de correspondance en-tête réel → nom normalisé (gère majuscules/espaces)
    header_map = {h.strip().lower(): h for h in reader.fieldnames if h}

    existing_emails = set(
        Person.objects.for_org(org).values_list("email", flat=True)
    )
    seen_in_file = set()

    created = 0
    skipped_existing = 0
    skipped_quota = 0
    row_errors = []
    to_create = []

    for line_number, row in enumerate(reader, start=2):  # ligne 1 = en-tête
        first_name = (row.get(header_map["first_name"]) or "").strip()
        last_name = (row.get(header_map["last_name"]) or "").strip()
        email = (row.get(header_map["email"]) or "").strip().lower()
        person_type_raw = row.get(header_map.get("person_type", ""), "") if "person_type" in header_map else ""

        if not any([first_name, last_name, email]):
            continue  # ligne vide — ignorée silencieusement

        if not first_name or not last_name or not email:
            row_errors.append((line_number, _("Prénom, nom et email sont obligatoires.")))
            continue

        try:
            validate_email(email)
        except ValidationError:
            row_errors.append((line_number, _("Adresse email invalide : %(email)s") % {"email": email}))
            continue

        if email in existing_emails:
            skipped_existing += 1
            continue
        if email in seen_in_file:
            row_errors.append((line_number, _("Email en doublon dans le fichier : %(email)s") % {"email": email}))
            continue
        seen_in_file.add(email)

        if max_new is not None and len(to_create) >= max_new:
            skipped_quota += 1
            continue

        to_create.append(Person(
            org=org,
            email=email,
            first_name=first_name,
            last_name=last_name,
            person_type=_normalize_person_type(person_type_raw),
            created_by=user,
        ))

    if to_create:
        Person.objects.bulk_create(to_create)
        created = len(to_create)

    return {
        "created": created,
        "skipped_existing": skipped_existing,
        "skipped_quota": skipped_quota,
        "row_errors": row_errors,
    }
