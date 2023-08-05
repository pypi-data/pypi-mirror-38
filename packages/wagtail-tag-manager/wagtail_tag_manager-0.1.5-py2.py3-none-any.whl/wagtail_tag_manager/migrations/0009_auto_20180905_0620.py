# Generated by Django 2.0.6 on 2018-09-05 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_tag_manager', '0008_auto_20180905_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='passive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_loading',
            field=models.CharField(choices=[('instant_load', 'Instant'), ('lazy_load', 'Lazy')], default='instant_load', max_length=12),
        ),
    ]
