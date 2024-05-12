# Generated by Django 4.2.6 on 2024-01-23 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_room_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='enrolled_classes', to='accounts.studentprofile'),
        ),
        migrations.AlterField(
            model_name='room',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taught_classes', to='accounts.teacherprofile'),
        ),
    ]