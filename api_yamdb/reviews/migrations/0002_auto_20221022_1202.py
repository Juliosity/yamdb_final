# Generated by Django 2.2.16 on 2022-10-22 09:02

import django.core.validators
from django.db import migrations, models

import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': 'comments', 'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': 'reviews', 'ordering': ('-pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Рейтинг не может быть менее 1'), django.core.validators.MaxValueValidator(limit_value=10, message='Рейтинг не может быть более 10')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, validators=[reviews.validators.DynamicMaxYearValidator(reviews.validators.current_year, message='Не возможно добавить еще не вышедшие произведения')], verbose_name='год'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Админ'), ('user', 'Пользователь'), ('moderator', 'Модератор')], default='user', max_length=9, verbose_name='Уровень доступа'),
        ),
    ]
