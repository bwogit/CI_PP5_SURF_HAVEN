# Generated by Django 3.2.21 on 2023-09-26 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_alter_order_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(default='', max_length=40),
        ),
    ]
