# Generated by Django 2.0.2 on 2018-03-13 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_kairos', '0006_auto_20180313_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='image',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
