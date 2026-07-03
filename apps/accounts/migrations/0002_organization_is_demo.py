from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="is_demo",
            field=models.BooleanField(
                default=False,
                help_text="Org de démo publique — données fictives, emails bloqués, reset périodique.",
                verbose_name="organisation de démonstration",
            ),
        ),
    ]
