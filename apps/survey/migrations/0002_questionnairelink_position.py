import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0001_initial"),
        ("positions", "0002_position_department_fk_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionnairelink",
            name="position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="questionnaire_links",
                to="positions.position",
                verbose_name="poste",
            ),
        ),
    ]
