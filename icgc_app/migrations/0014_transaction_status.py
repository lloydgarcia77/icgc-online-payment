# Generated by Django 3.2.14 on 2022-11-09 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icgc_app', '0013_transaction_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]