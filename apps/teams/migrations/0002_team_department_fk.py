import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_initial"),
        ("departments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="teams",
                to="departments.department",
                verbose_name="département",
            ),
        ),
    ]
