# Generated by Django 5.0.6 on 2024-11-09 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oc', '0005_pdfdocument_alter_cliente_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompra',
            name='cantidad',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordencompra',
            name='precio_unitario',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='afiliado',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='domicilioafiliado',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordencompra',
            name='nrocompulsa',
            field=models.CharField(blank=True, default='4500', max_length=20, null=True),
        ),
    ]