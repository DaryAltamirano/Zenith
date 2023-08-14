# Generated by Django 4.2 on 2023-08-13 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('equipref', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HaystackTag',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('geoAddr', models.CharField(max_length=255)),
                ('geoCoord', models.CharField(max_length=255)),
                ('tz', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spaceref', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sensor_driver.zone')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('created_at', models.DateField(auto_created=True, auto_now=True, verbose_name='Fecha de creacion')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('series', models.CharField(max_length=100)),
                ('format', models.JSONField()),
                ('protocol', models.CharField(max_length=50)),
                ('equip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sensor_driver.equip')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('created_at', models.DateField(auto_created=True, auto_now=True, verbose_name='Fecha de creacion')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timeline', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='sensor_driver.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('connection', models.JSONField(null=True)),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='sensor_driver.sensor')),
            ],
        ),
        migrations.AddField(
            model_name='equip',
            name='space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sensor_driver.space'),
        ),
    ]