# Generated by Django 5.0.6 on 2024-05-29 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_profilecompany_content_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilecompany',
            name='custom_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
