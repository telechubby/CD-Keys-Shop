# Generated by Django 4.2.4 on 2023-08-31 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdkeyshop', '0005_alter_category_id_alter_order_id_alter_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trendingproduct',
            old_name='product_id',
            new_name='product',
        ),
    ]
