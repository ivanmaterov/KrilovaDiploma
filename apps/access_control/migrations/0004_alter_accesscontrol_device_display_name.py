# Generated by Django 4.2.7 on 2023-12-01 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access_control', '0003_alter_accesscontrol_soi_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesscontrol',
            name='device_display_name',
            field=models.CharField(blank=True, help_text='Отображаемое имя устройства', max_length=512, verbose_name='Отображаемое имя устройства'),
        ),
    ]
