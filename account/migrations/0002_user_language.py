# Generated by Django 4.1.7 on 2023-03-29 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('uz', "O'zbek"), ('ru', 'Русский')], max_length=50, null=True),
        ),
    ]
