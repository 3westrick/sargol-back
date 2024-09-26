# Generated by Django 5.0.2 on 2024-08-05 11:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('coupon', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='basket', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True)),
                ('coupons', models.ManyToManyField(blank=True, null=True, to='coupon.coupon')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('post_code', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('bin', 'bin'), ('processing', 'processing'), ('on_hold', 'on_hold'), ('completed', 'completed'), ('canceled', 'canceled'), ('failed', 'failed'), ('refunded', 'refunded'), ('pending', 'pending')], default='processing', max_length=50)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('coupons', models.ManyToManyField(related_name='orders', to='coupon.coupon')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('backorder', models.BooleanField(default=False)),
                ('notify', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
