# Generated by Django 5.0.3 on 2024-04-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_employeeformmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeformmodel',
            name='status',
            field=models.CharField(choices=[('ACCEPTED', 'accepted'), ('REJECTED', 'rejected'), ('PENDING', 'pending'), ('PROCESSED', 'processed'), ('REJECTEDF', 'rejectedbyfinance')], default='PENDING', max_length=20),
        ),
    ]