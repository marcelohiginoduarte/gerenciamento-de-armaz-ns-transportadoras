# Generated by Django 5.1.2 on 2024-10-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armazenamento', '0003_rename_nome_produto_nf_rename_sku_produto_cidade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='cliente',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
