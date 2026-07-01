"""
Data migration: convert Position.department (CharField) to Department FK objects.
Runs before positions migration adds the FK column.
"""
from django.db import migrations


def create_departments_from_positions(apps, schema_editor):
    Position = apps.get_model("positions", "Position")
    Department = apps.get_model("departments", "Department")

    seen = set()
    for pos in Position.objects.exclude(department="").select_related("org"):
        key = (pos.org_id, pos.department)
        if key not in seen:
            Department.objects.get_or_create(
                org=pos.org,
                name_fr=pos.department,
            )
            seen.add(key)


def reverse_migration(apps, schema_editor):
    # On ne supprime pas les départements créés — trop risqué en rollback
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0001_initial"),
        ("positions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_departments_from_positions, reverse_migration),
    ]
