# Generated by Django 5.1.2 on 2024-10-17 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armazenamento', '0008_espacoarmazenamento_vaga_alter_produto_cidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='espacoarmazenamento',
            name='vaga',
            field=models.BooleanField(default=True),
        ),
    ]
