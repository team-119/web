# Generated by Django 3.1.2 on 2020-10-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emerapp', '0008_auto_20201026_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='hos',
            field=models.CharField(default='-', max_length=1),
        ),
    ]
