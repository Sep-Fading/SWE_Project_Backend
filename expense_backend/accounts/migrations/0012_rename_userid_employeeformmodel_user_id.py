# Generated by Django 4.2.11 on 2024-04-07 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_employeeformmodel_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeformmodel',
            old_name='userID',
            new_name='user_id',
        ),
    ]
