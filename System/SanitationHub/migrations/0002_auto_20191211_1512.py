# Generated by Django 2.2.5 on 2019-12-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SanitationHub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='codeID',
            field=models.CharField(max_length=200, verbose_name='OrgID'),
        ),
    ]
