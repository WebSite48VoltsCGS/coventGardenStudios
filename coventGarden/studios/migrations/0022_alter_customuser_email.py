# Generated by Django 4.2.2 on 2023-07-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0021_alter_customgroup_genre_alter_customgroup_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
