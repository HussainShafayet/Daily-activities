# Generated by Django 3.1 on 2020-10-10 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20201010_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='image.jpg', null=True, upload_to='images/'),
        ),
    ]
