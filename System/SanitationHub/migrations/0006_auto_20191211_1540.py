# Generated by Django 2.2.5 on 2019-12-11 15:40

import SanitationHub.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SanitationHub', '0005_auto_20191211_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='codeID',
            field=models.CharField(default=SanitationHub.models.generateRandomValue, max_length=6, verbose_name='OrgID'),
        ),
    ]
