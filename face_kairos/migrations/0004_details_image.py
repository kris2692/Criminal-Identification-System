# Generated by Django 2.0.2 on 2018-03-13 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_kairos', '0003_auto_20180312_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
