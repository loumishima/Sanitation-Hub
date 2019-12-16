# Generated by Django 2.2.5 on 2019-12-13 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SanitationHub', '0007_auto_20191211_1617'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statsresumed',
            name='count',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='maxVal',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='mean',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='minVal',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='perc25',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='perc50',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='perc75',
        ),
        migrations.RemoveField(
            model_name='statsresumed',
            name='std',
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='capacity_mean',
            field=models.FloatField(blank=True, null=True, verbose_name='Capacity Avg'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='capacity_std',
            field=models.FloatField(blank=True, null=True, verbose_name='Capacity Stdev'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='last_cleaned_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Cleaning time Stdev'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='last_cleaned_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Cleaning time Min'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='number_toilets',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of toilets'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='people_using_max',
            field=models.FloatField(blank=True, null=True, verbose_name='Usage Max'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='people_using_mean',
            field=models.FloatField(blank=True, null=True, verbose_name='Usage Mean'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='people_using_min',
            field=models.FloatField(blank=True, null=True, verbose_name='Usage Min'),
        ),
        migrations.AddField(
            model_name='statsresumed',
            name='people_using_std',
            field=models.FloatField(blank=True, null=True, verbose_name='Usage Stdev'),
        ),
    ]
