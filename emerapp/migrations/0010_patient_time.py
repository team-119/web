# Generated by Django 3.1.2 on 2020-10-26 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emerapp', '0009_auto_20201026_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='time',
            field=models.CharField(default='0', max_length=5),
        ),
    ]
