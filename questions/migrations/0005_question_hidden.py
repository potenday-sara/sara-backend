# Generated by Django 4.2.7 on 2023-11-24 05:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("questions", "0004_ai"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="hidden",
            field=models.BooleanField(default=False),
        ),
    ]
