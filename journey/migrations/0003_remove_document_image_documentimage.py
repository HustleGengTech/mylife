# Generated by Django 5.0.7 on 2024-08-21 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0002_emergencycontact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='image',
        ),
        migrations.CreateModel(
            name='DocumentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='documents/')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='journey.document')),
            ],
        ),
    ]
