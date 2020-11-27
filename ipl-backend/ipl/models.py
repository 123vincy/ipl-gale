# coding: utf-8
from postgres_copy import CopyManager
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, UniqueConstraint, text, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
#  Override user models from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

Base = declarative_base()


class Matches(models.Model):
    class Meta:
        db_table = "matches"

    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.CharField(max_length=50, null=True)
    date = models.DateField()
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    toss_winner = models.CharField(max_length=50, null=True)
    toss_decision = models.CharField(max_length=50, null=True)
    result = models.CharField(max_length=50, null=True)
    dl_applied = models.IntegerField()
    winner = models.CharField(max_length=50, null=True)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_match = models.CharField(max_length=50, null=True)
    venue = models.CharField(max_length=50, null=True)
    umpire1 = models.CharField(max_length=50, null=True)
    umpire2 = models.CharField(max_length=50, null=True)
    umpire3 = models.IntegerField(null=True)

    objects = CopyManager()


class Deliveries(models.Model):
    class Meta:
        db_table = "deliveries"

    match_id = models.ForeignKey(
        Matches, related_name='deliveries', on_delete=models.CASCADE)
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=50)
    bowling_team = models.CharField(max_length=50)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=50)
    non_striker = models.CharField(max_length=50, null=True)
    bowler = models.CharField(max_length=50)
    is_super_over = models.IntegerField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=50, null=True)
    dismissal_kind = models.CharField(max_length=50, null=True)
    fielder = models.CharField(max_length=50, null=True)

    objects = CopyManager()
