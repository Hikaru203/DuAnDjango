# Generated by Django 4.2.11 on 2024-03-15 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
