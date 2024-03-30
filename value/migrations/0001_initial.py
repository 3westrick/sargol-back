# Generated by Django 5.0.2 on 2024-03-30 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("attribute", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Value",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("slug", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "color",
                    models.CharField(blank=True, default=None, max_length=9, null=True),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="values",
                        to="attribute.attribute",
                    ),
                ),
            ],
        ),
    ]
