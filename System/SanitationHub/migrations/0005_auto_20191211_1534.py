# Generated by Django 2.2.5 on 2019-12-11 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SanitationHub', '0004_auto_20191211_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='codeID',
            field=models.CharField(max_length=20, verbose_name='OrgID'),
        ),
    ]
