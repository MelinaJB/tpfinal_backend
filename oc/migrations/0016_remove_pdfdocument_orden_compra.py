# Generated by Django 5.0.6 on 2024-11-10 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oc', '0015_alter_pdfdocument_orden_compra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdfdocument',
            name='orden_compra',
        ),
    ]
