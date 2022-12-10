# Generated by Django 4.1 on 2022-11-29 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libApp', '0002_alter_person_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('book_types', models.CharField(choices=[('E', 'education'), ('M', 'mangas'), ('MM', 'mm_books'), ('H', 'history'), ('HE', 'health'), ('N', 'novel')], max_length=200)),
                ('date', models.DateField(auto_now=True)),
                ('book_cover', models.ImageField(upload_to='covers')),
                ('book_pdf', models.FileField(upload_to='pdfs')),
            ],
        ),
    ]