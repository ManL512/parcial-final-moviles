# Generated by Django 5.0.4 on 2024-05-22 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_user_fcm_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.CharField(blank=True, choices=[('photo1.jpg', 'Photo 1'), ('photo2.jpg', 'Photo 2'), ('photo3.jpg', 'Photo 3')], max_length=255, null=True),
        ),
    ]
