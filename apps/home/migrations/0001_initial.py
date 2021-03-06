# Generated by Django 2.2.4 on 2019-09-21 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('content_html', models.TextField(blank=True, null=True)),
                ('add_time', models.DateTimeField(blank=True, null=True)),
                ('platform', models.CharField(blank=True, max_length=100, null=True)),
                ('platform_url', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
    ]
