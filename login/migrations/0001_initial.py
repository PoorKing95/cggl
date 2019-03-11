# Generated by Django 2.1.7 on 2019-03-11 16:37

from django.db import migrations, models
import django.db.models.deletion
import login.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('uid', models.BigAutoField(primary_key=True, serialize=False)),
                ('uaccount', models.CharField(max_length=100, unique=True)),
                ('unamech', models.CharField(max_length=100)),
                ('unameen', models.CharField(max_length=100)),
                ('upassword', models.CharField(max_length=100)),
                ('umail', models.CharField(max_length=100, unique=True)),
                ('uphone', login.models.MyCharField(max_length=11)),
                ('uqq', models.CharField(max_length=100, unique=True)),
                ('uall', models.BooleanField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('aid', models.BigAutoField(primary_key=True, serialize=False)),
                ('afnamech', models.CharField(max_length=1000)),
                ('alnamech', models.CharField(max_length=1000)),
                ('anamech', models.CharField(max_length=1000)),
                ('afnameen', models.CharField(max_length=1000)),
                ('alnameen', models.CharField(max_length=1000)),
                ('anameen', models.CharField(max_length=1000)),
                ('amail', models.EmailField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='AuthorCompany',
            fields=[
                ('acid', models.BigAutoField(primary_key=True, serialize=False)),
                ('acorder', models.SmallIntegerField()),
                ('accurrent', models.BooleanField()),
                ('author', models.ForeignKey(db_column='aid', on_delete=django.db.models.deletion.CASCADE, to='login.Author')),
            ],
            options={
                'db_table': 'author_company',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('cid', models.BigAutoField(primary_key=True, serialize=False)),
                ('cnamech1', models.CharField(max_length=1000)),
                ('cnameeg1', models.CharField(max_length=1000)),
                ('cnamech2', models.CharField(max_length=1000)),
                ('cnameeg2', models.CharField(max_length=1000)),
                ('czipcode', models.CharField(max_length=1000)),
                ('addressch', models.CharField(max_length=1000)),
                ('addressen', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('pid', models.BigAutoField(primary_key=True, serialize=False)),
                ('pname', models.CharField(max_length=1000)),
                ('ptype', models.CharField(max_length=10)),
                ('pifpub', models.BooleanField()),
                ('pplace', models.CharField(max_length=1000)),
                ('ppub', models.CharField(max_length=1000)),
                ('pyear', models.IntegerField()),
                ('ppage', models.BigIntegerField()),
                ('ppath', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'paper',
            },
        ),
        migrations.CreateModel(
            name='PaperAuthor',
            fields=[
                ('paid', models.BigAutoField(primary_key=True, serialize=False)),
                ('paorder', models.SmallIntegerField()),
                ('pacommunication', models.BooleanField()),
                ('pacorder', models.SmallIntegerField()),
                ('author', models.ForeignKey(db_column='aid', on_delete=django.db.models.deletion.CASCADE, to='login.Author')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Company')),
                ('paper', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='login.Paper')),
            ],
            options={
                'db_table': 'paper_author',
            },
        ),
        migrations.AddField(
            model_name='authorcompany',
            name='company',
            field=models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to='login.Company'),
        ),
    ]
