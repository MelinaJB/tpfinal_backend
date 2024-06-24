# Generated by Django 5.0.6 on 2024-06-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompra',
            name='entrega_unica',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='estado',
            field=models.CharField(choices=[('certificado', 'Certificado'), ('baja', 'Baja'), ('entregada', 'Entregada'), ('pendiente', 'Pendiente'), ('activa', 'Activa')], default='pendiente', max_length=20),
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='numero',
            field=models.CharField(default='4500', max_length=20, unique=True),
        ),
    ]
