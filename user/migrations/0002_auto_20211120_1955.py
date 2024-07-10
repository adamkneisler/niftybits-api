# Generated by Django 3.2.2 on 2021-11-20 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.niftyuser'),
        ),
        migrations.AlterField(
            model_name='niftyuser',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='withdrawl',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.niftyuser'),
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ledger_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default=None, max_length=32)),
                ('amount', models.FloatField(default=0.0)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('deposit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.deposit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.niftyuser')),
                ('withdrawl', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.withdrawl')),
            ],
        ),
    ]
