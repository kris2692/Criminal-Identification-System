# Generated by Django 2.0.2 on 2018-03-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_kairos', '0008_auto_20180314_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
