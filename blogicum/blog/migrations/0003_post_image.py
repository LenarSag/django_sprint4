# Generated by Django 3.2.16 on 2024-02-08 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20240207_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Картинка'),
        ),
    ]
