# Generated by Django 2.1.3 on 2019-01-23 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bisonMatchApp', '0002_imageupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='media',
            field=models.FileField(upload_to='user_profiles'),
        ),
    ]