# Generated by Django 2.2.28 on 2023-03-14 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20230314_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customercart',
            name='addedon',
        ),
        migrations.RemoveField(
            model_name='customercart',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='customercart',
            name='product',
        ),
    ]