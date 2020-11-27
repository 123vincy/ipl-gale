# Generated by Django 3.1.3 on 2020-11-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchid', models.IntegerField()),
                ('inning', models.IntegerField()),
                ('batting_team', models.CharField(max_length=50)),
                ('bowling_team', models.CharField(max_length=50)),
                ('over', models.IntegerField()),
                ('ball', models.IntegerField()),
                ('batsman', models.CharField(max_length=50)),
                ('non_striker', models.CharField(max_length=50)),
                ('bowler', models.CharField(max_length=50)),
                ('is_super_over', models.IntegerField()),
                ('wide_runs', models.IntegerField()),
                ('bye_runs', models.IntegerField()),
                ('legbye_runs', models.IntegerField()),
                ('noball_runs', models.IntegerField()),
                ('penalty_runs', models.IntegerField()),
                ('batsman_runs', models.IntegerField()),
                ('extra_runs', models.IntegerField()),
                ('total_runs', models.IntegerField()),
                ('player_dismissed', models.CharField(max_length=50)),
                ('dismissal_kind', models.CharField(max_length=50)),
                ('fielder', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'deliveries',
            },
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('season', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('team1', models.CharField(max_length=50)),
                ('team2', models.CharField(max_length=50)),
                ('toss_winner', models.CharField(max_length=50)),
                ('toss_decision', models.CharField(max_length=50)),
                ('result', models.CharField(max_length=50)),
                ('dl_applied', models.IntegerField()),
                ('winner', models.CharField(max_length=50)),
                ('win_by_runs', models.IntegerField()),
                ('win_by_wickets', models.IntegerField()),
                ('player_of_the_match', models.CharField(max_length=50)),
                ('venue', models.CharField(max_length=50)),
                ('umpire1', models.CharField(max_length=50)),
                ('umpire2', models.CharField(max_length=50)),
                ('umpire3', models.IntegerField()),
            ],
            options={
                'db_table': 'matches',
            },
        ),
        migrations.DeleteModel(
            name='Dreamreal',
        ),
    ]