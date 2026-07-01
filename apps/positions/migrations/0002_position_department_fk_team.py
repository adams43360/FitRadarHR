"""
Migration: replace Position.department (CharField) with FK to Department,
and add optional FK to Team.

The data migration (departments/0002) must run first to create Department objects
from existing text values.
"""
import django.db.models.deletion
from django.db import migrations, models


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
        migrations.RunSQL(
            sql="""
                UPDATE positions_position p
                SET department_fk_id = d.id
                FROM departments_department d
                WHERE d.org_id = p.org_id
                  AND d.name_fr = p.department
                  AND p.department != '';
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
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
