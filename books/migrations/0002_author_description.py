# Generated by Django 3.2.2 on 2021-06-16 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
