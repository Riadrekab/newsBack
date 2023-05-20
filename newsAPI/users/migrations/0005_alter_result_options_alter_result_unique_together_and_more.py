# Generated by Django 4.2.1 on 2023-05-20 18:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_result_author_remove_result_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together={('profile', 'title')},
        ),
        migrations.CreateModel(
            name='historyResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('input', models.CharField(blank=True, max_length=250, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
