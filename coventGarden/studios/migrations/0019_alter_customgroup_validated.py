# Generated by Django 4.2.2 on 2023-07-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0018_customgroup_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customgroup',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='Vérifié'),
        ),
    ]