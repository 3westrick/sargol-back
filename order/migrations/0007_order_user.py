# Generated by Django 5.0.2 on 2024-08-08 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_rename_post_code_order_postcode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
