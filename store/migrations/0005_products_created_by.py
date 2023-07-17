# Generated by Django 4.2.1 on 2023-06-06 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0004_remove_products_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='created_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='product_creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
