import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name_fr", models.CharField(max_length=255, verbose_name="nom (FR)")),
                ("name_en", models.CharField(blank=True, max_length=255, verbose_name="nom (EN)")),
                ("description", models.TextField(blank=True, verbose_name="description")),
                ("is_archived", models.BooleanField(default=False, verbose_name="archivé")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="departments",
                        to="accounts.organization",
                        verbose_name="organisation",
                    ),
                ),
            ],
            options={
                "verbose_name": "département",
                "verbose_name_plural": "départements",
                "ordering": ["name_fr"],
                "unique_together": {("org", "name_fr")},
            },
        ),
    ]
