# Generated by Django 4.0.7 on 2023-11-06 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='items'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='authentication.users'),
            preserve_default=False,
        ),
    ]
