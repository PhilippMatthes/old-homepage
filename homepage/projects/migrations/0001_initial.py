# Generated by Django 2.2.3 on 2019-08-07 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siri', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('readable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='siri.Readable')),
                ('thumbnail', models.ImageField(upload_to='projects/')),
                ('title', models.TextField()),
                ('description', models.TextField()),
            ],
            bases=('siri.readable',),
        ),
    ]
