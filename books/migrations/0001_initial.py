# Generated by Django 3.2.2 on 2021-06-09 19:28

import books.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a book genre (e.g. sci-fi, comedy)', max_length=50, unique=True, verbose_name='Genre name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('plot', models.TextField(blank=True, null=True, verbose_name='Plot')),
                ('release_date', models.DateField(blank=True, help_text='Please use the following format: <em>YYYY-MM-DD</em>.', null=True, verbose_name='Release date')),
                ('runtime', models.IntegerField(blank=True, help_text='Please enter an integer value (minutes)', null=True, verbose_name='Pages')),
                ('rate', models.FloatField(default=5.0, help_text='Please enter an float value (range 1.0 - 10.0)', null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)], verbose_name='Rate')),
                ('poster', models.ImageField(blank=True, null=True, upload_to=books.models.poster_path, verbose_name='Poster')),
                ('genres', models.ManyToManyField(help_text='Select a genre for this book', to='books.Genre')),
            ],
            options={
                'ordering': ['-release_date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(null=True, upload_to=books.models.attachment_path, verbose_name='File')),
                ('type', models.CharField(blank=True, choices=[('audio', 'Audio'), ('image', 'Image'), ('text', 'Text'), ('video', 'Video'), ('other', 'Other')], default='image', help_text='Select allowed attachment type', max_length=5, verbose_name='Attachment type')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
            options={
                'order_with_respect_to': 'book',
            },
        ),
    ]