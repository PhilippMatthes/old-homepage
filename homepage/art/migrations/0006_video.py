# Generated by Django 2.2.3 on 2019-08-12 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0005_auto_20190811_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('artwork_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='art.Artwork')),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
            ],
            bases=('art.artwork',),
        ),
    ]
