# Generated by Django 3.1 on 2020-10-10 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20201011_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='static/images/favicon.png', null=True, upload_to='images/'),
        ),
    ]