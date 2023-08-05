# Generated by Django 2.1.1 on 2018-09-08 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_musician_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='instrument',
            field=models.CharField(choices=[('GUITAR', 'Guitar'), ('VOICE', 'Voice'), ('DRUM', 'Drum'), ('SAX', 'Saxophone')], max_length=100),
        ),
    ]
