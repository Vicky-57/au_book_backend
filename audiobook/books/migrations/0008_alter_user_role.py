# Generated by Django 5.1 on 2024-09-02 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0007_alter_shloka_audio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="books.role",
            ),
        ),
    ]