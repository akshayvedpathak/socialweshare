# Generated by Django 4.1.2 on 2022-11-27 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_alter_userinfo_cover_alter_userinfo_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='cover',
            field=models.ImageField(default='pqr.jpg', upload_to='media/Images'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='profil',
            field=models.ImageField(default='abc.jpg', upload_to='media/Images'),
        ),
    ]
