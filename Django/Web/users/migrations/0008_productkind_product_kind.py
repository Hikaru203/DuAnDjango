# Generated by Django 4.2.11 on 2024-03-16 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='kind',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.productkind'),
        ),
    ]
