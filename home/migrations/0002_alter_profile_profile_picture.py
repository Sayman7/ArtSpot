# Generated by Django 5.1.6 on 2025-03-18 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='static/default.jpg', upload_to='profile_pics/'),
        ),
    ]
