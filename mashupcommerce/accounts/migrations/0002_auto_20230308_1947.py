# Generated by Django 2.2.28 on 2023-03-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_picture',
            field=models.FileField(upload_to='pics'),
        ),
    ]