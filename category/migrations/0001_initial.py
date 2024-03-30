# Generated by Django 5.0.2 on 2024-03-30 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("slug", models.CharField(max_length=50)),
                ("is_active", models.BooleanField(default=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="category.category",
                    ),
                ),
            ],
        ),
    ]
