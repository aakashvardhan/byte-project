# Generated by Django 2.0.4 on 2018-05-21 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20180519_1206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='attending',
            new_name='attending_event',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='not_attending',
            new_name='not_attending_event',
        ),
        migrations.AlterField(
            model_name='attending',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.Schedule'),
        ),
    ]
