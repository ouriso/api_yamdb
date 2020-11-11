# Generated by Django 3.0.5 on 2020-11-10 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.Title'),
        ),
        migrations.AlterUniqueTogether(
            name='genre',
            unique_together={('name', 'slug')},
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Review'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'slug')},
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 10)), name='A rating value is valid between 1 and 10'),
        ),
        migrations.AlterUniqueTogether(
            name='title',
            unique_together={('name', 'year')},
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('score__gte', 1), ('score__lte', 10)), name='A score value is valid between 1 and 10'),
        ),
    ]
