# Generated by Django 2.0.6 on 2018-09-13 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_tag_manager', '0014_auto_20180906_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['tag_loading', '-active', 'tag_location', '-priority']},
        ),
        migrations.AddField(
            model_name='tag',
            name='priority',
            field=models.SmallIntegerField(default=0, help_text='Define how early on this tag should load as compared to other tags. A higher number will load sooner. For example:<br/> - A tag with a priority of 3 will load before a tag with priority 1.<br/> - A tag with a priority 0 will load before a tag with priority -1.<br/><em>Please note that with instanly loading tags, the priority is only compared to tags that load in the same document location.</em>'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_location',
            field=models.CharField(choices=[('0_top_head', 'Top of head tag'), ('1_bottom_head', 'Bottom of head tag'), ('2_top_body', 'Top of body tag'), ('3_bottom_body', 'Bottom of body tag')], default='0_top_head', help_text='Where in the document this tag will be inserted. Only applicable for tags that load instantly.', max_length=12),
        ),
    ]
