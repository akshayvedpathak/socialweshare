# Generated by Django 4.1.2 on 2022-12-06 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_alter_userinfo_cover_alter_userinfo_profil'),
    ]

    operations = [
        migrations.CreateModel(
            name='userpost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=150)),
                ('postphoto', models.ImageField(upload_to='Images')),
            ],
            options={
                'db_table': 'userpost',
            },
        ),
    ]
