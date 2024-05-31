# Generated by Django 5.0.6 on 2024-05-22 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_service', '0005_company_niche'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='niche',
            field=models.CharField(choices=[('EC', 'Electronics & Computers'), ('FU', 'Furniture'), ('HP', 'Home Products'), ('CS', 'Cosmetics, skin & hair care'), ('TC', 'Toys and products for children'), ('CS', 'Clothes and shoes'), ('SH', 'Sports and hobbies'), ('FD', 'Food and drink'), ('OT', 'Others')], default='OT', max_length=2),
        ),
    ]
