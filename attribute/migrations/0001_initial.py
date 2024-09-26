# Generated by Django 5.0.2 on 2024-08-05 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('color', 'color'), ('normal', 'normal')], default='normal', max_length=20)),
            ],
        ),
    ]
