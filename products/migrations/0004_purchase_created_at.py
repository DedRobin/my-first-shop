# Generated by Django 4.1.1 on 2022-09-14 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
    ]
