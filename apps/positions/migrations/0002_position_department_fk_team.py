"""
Migration: replace Position.department (CharField) with FK to Department,
and add optional FK to Team.

The data migration (departments/0002) must run first to create Department objects
from existing text values.
"""
import django.db.models.deletion
from django.db import migrations, models


def populate_department_fk(apps, schema_editor):
    """Relie chaque poste au Department créé depuis l'ancien champ texte.

    Version ORM (portable PostgreSQL/SQLite) de l'ancien UPDATE ... FROM.
    """
    Position = apps.get_model("positions", "Position")
    Department = apps.get_model("departments", "Department")

    for pos in Position.objects.exclude(department=""):
        dept = Department.objects.filter(
            org_id=pos.org_id, name_fr=pos.department
        ).first()
        if dept:
            pos.department_fk_id = dept.id
            pos.save(update_fields=["department_fk"])


class Migration(migrations.Migration):

    dependencies = [
        ("positions", "0001_initial"),
        ("departments", "0002_data_migrate_position_departments"),
        ("teams", "0001_initial"),
    ]

    operations = [
        # Step 1: add the new FK column (nullable)
        migrations.AddField(
            model_name="position",
            name="department_fk",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="positions",
                to="departments.department",
                verbose_name="département",
            ),
        ),
        # Step 2: populate it from existing text field
        migrations.RunPython(populate_department_fk, migrations.RunPython.noop),
        # Step 3: drop old text column
        migrations.RemoveField(model_name="position", name="department"),
        # Step 4: rename new column to 'department'
        migrations.RenameField(
            model_name="position",
            old_name="department_fk",
            new_name="department",
        ),
        # Step 5: add team FK
        migrations.AddField(
            model_name="position",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="positions",
                to="teams.team",
                verbose_name="équipe cible",
            ),
        ),
    ]
