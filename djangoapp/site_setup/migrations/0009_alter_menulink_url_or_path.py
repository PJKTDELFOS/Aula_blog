# Generated by Django 5.1.4 on 2024-12-13 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0008_alter_sitesetup_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menulink',
            name='url_or_path',
            field=models.CharField(max_length=2048),
        ),
    ]
