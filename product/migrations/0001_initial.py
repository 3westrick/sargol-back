# Generated by Django 5.0.2 on 2024-03-17 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("attribute", "0001_initial"),
        ("category", "0001_initial"),
        ("value", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("slug", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "short_description",
                    models.TextField(blank=True, default=None, null=True),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("regular_price", models.IntegerField(default=0)),
                ("sale_price", models.IntegerField(default=0)),
                ("tax_status", models.CharField(max_length=50)),
                ("tax_class", models.CharField(max_length=50)),
                ("sku", models.CharField(max_length=50)),
                ("mpn", models.CharField(max_length=50)),
                ("stock_management", models.BooleanField(default=False)),
                ("stock_status", models.CharField(max_length=50)),
                ("sold_individually", models.BooleanField(default=False)),
                ("stock", models.IntegerField(default=0)),
                ("unit", models.CharField(max_length=50)),
                ("weight", models.IntegerField(default=0)),
                ("length", models.IntegerField(default=0)),
                ("width", models.IntegerField(default=0)),
                ("height", models.IntegerField(default=0)),
                ("shipping_class", models.CharField(max_length=50)),
                (
                    "attributes",
                    models.ManyToManyField(
                        related_name="products", to="attribute.attribute"
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="products", to="category.category"
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="variants",
                        to="product.product",
                    ),
                ),
                (
                    "values",
                    models.ManyToManyField(related_name="products", to="value.value"),
                ),
                (
                    "variantAttributes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="variant_products",
                        to="attribute.attribute",
                    ),
                ),
                (
                    "visibleAttributes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="visible_products",
                        to="attribute.attribute",
                    ),
                ),
            ],
        ),
    ]