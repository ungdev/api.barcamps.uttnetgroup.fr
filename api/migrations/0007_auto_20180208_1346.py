# Generated by Django 2.0.1 on 2018-02-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_delete_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talk',
            name='slides_name',
        ),
        migrations.AddField(
            model_name='talk',
            name='slides',
            field=models.FileField(null=True, upload_to='uploads/'),
        ),
    ]
