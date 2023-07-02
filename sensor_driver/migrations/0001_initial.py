# Generated by Django 4.2 on 2023-07-02 03:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('headers', models.CharField(help_text='Enter field documentation', max_length=2000, null=True)),
                ('format', models.CharField(help_text='Enter field documentation', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter field documentation', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('created_at', models.DateField(auto_created=True, auto_now=True, verbose_name='Fecha de creacion')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Enter field documentation', max_length=20)),
                ('series', models.CharField(help_text='Enter field documentation', max_length=20)),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='Enter field documentation', unique=True)),
                ('protocol', models.CharField(choices=[('HTTP', 'Http'), ('MQTT', 'Mqtt')], default='HTTP', help_text='Enter field documentation', max_length=20)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sensor_driver.request')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sensor_driver.zone')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('created_at', models.DateField(auto_created=True, auto_now=True, verbose_name='Fecha de creacion')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uri', models.CharField(help_text='Enter field documentation', max_length=20)),
                ('timeMeasure', models.CharField(help_text='Enter field documentation', max_length=20)),
                ('timeline', models.CharField(help_text='Enter field documentation', max_length=20)),
                ('sensor_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sensor_driver.sensor')),
            ],
        ),
    ]
