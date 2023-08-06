from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import horizon.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcreteModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pizza', models.CharField(max_length=15, unique=True)),
                ('potate', models.CharField(max_length=15, unique=True)),
                ('coke', models.CharField(max_length=15, unique=True)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'horizontal_group': 'b',
                'horizontal_key': 'user',
            },
            managers=[
                ('objects', horizon.manager.HorizontalManager()),
            ],
        ),
        migrations.CreateModel(
            name='HorizontalMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=15)),
                ('key', models.CharField(max_length=32)),
                ('index', models.PositiveSmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManyModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'horizontal_group': 'a',
                'horizontal_key': 'user',
            },
            managers=[
                ('objects', horizon.manager.HorizontalManager()),
            ],
        ),
        migrations.CreateModel(
            name='OneModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('spam', models.CharField(max_length=15)),
                ('egg', models.CharField(default=None, max_length=15, null=True)),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'horizontal_group': 'a',
                'horizontal_key': 'user',
            },
            managers=[
                ('objects', horizon.manager.HorizontalManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProxyBaseModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sushi', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'horizontal_group': 'b',
                'horizontal_key': 'user',
            },
            managers=[
                ('objects', horizon.manager.HorizontalManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProxiedModel',
            fields=[
                ('proxybasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tests.ProxyBaseModel')),
                ('tempura', models.CharField(max_length=15, unique=True)),
                ('karaage', models.CharField(max_length=15, unique=True)),
            ],
            bases=('tests.proxybasemodel',),
            managers=[
                ('objects', horizon.manager.HorizontalManager()),
            ],
        ),
        migrations.AddField(
            model_name='proxybasemodel',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='manymodel',
            name='one',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.OneModel'),
        ),
        migrations.AddField(
            model_name='manymodel',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='horizontalmetadata',
            unique_together=set([('group', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='proxiedmodel',
            unique_together=set([('tempura', 'karaage')]),
        ),
        migrations.AlterUniqueTogether(
            name='concretemodel',
            unique_together=set([('pizza', 'coke')]),
        ),
    ]
