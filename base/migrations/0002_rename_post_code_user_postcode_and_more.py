# Generated by Django 5.0.2 on 2024-08-11 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='post_code',
            new_name='postcode',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='city',
            new_name='state',
        ),
    ]
