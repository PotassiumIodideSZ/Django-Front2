# Generated by Django 4.2.16 on 2024-10-10 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]