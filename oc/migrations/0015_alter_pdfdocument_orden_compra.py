# Generated by Django 5.0.6 on 2024-11-10 23:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oc', '0014_alter_pdfdocument_orden_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfdocument',
            name='orden_compra',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pdfs', to='oc.ordencompra'),
        ),
    ]