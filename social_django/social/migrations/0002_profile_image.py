# Generated by Django 5.0 on 2023-12-19 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='defaultuser.png', upload_to=''),
        ),
    ]
