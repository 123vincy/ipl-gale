import csv
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import json
from ipl.models import Deliveries, Matches

# using pandas for computing statistics
import numpy as np
import pandas as pd
from ipl.seralizers import *
from django.db.models import Max, Count, Value, Q, Sum
data_path = os.path.join(os.path.dirname(__file__), 'data/')

# ideally this should be a part of the pipeline
# Matches.objects.all().delete()
# Matches.objects.from_csv(data_path+'matches.csv')
# Deliveries.objects.all().delete()
# Deliveries.objects.from_csv(data_path+'deliveries.csv')
# batsman = df_del[['batsman', 'batsman_runs']]
# batsman = batsman.groupby(
#     'batsman')['batsman_runs'].sum().reset_index()
# batsman = batsman.sort_values(
#     by='batsman_runs', ascending=False).head(10)
# for index, row in batsman.iterrows():
#     runs.append({
#         'runs': row['batsman_runs'],
#         'batsman': row['batsman']
#     })


# serializer = MatchesSerializer(x, many=True)
# print (serializer.data)


@ api_view(['GET', 'POST'])
def seasons(request):
    try:
        df = pd.read_csv(data_path+'matches.csv', encoding='utf-8')
        df = df.replace({np.nan: None})

        unique_seasons = df['season'].unique().tolist()
        unique_seasons.sort(reverse=True)
        return JsonResponse({'seasons': unique_seasons})
    except Exception as e:
        return JsonResponse({'error': "Can't get the data: " + str(e)})


@ api_view(['GET', 'POST'])
def statistics(request):
    try:
        season = json.loads(request.body)['season']

        # •	Which team won by the highest margin of runs  for the season
        highest_margin_run = Matches.objects.values('winner', 'win_by_runs').filter(season=season, win_by_runs=Matches.objects.filter(
            season=season).aggregate(Max('win_by_runs'))['win_by_runs__max'])[0]['winner']

        # •	Which team won by the highest number of wickets for the season
        highest_margin_wickets = Matches.objects.filter(season=season).values('winner',
                                                                              'win_by_wickets').annotate(wins=Count('win_by_wickets')).order_by('-win_by_wickets')[:1][0]['winner']

        # •	Which team won the most number of tosses in the season
        most_tosses_won = Matches.objects.filter(season=season).values(
            'toss_winner').annotate(wins=Count('toss_winner')).order_by('-wins')[:1][0]['toss_winner']

        # • Which team won max matches in the whole season
        won_max_mat = Matches.objects.filter(season=season).values('winner').annotate(
            wins=Count('winner')).order_by('-wins')[:1][0]['winner']

        # •	Which location hosted most number of matches
        max_hosted_venue = Matches.objects.filter(season=season).values(
            'venue').annotate(total=Count('venue')).order_by('-total')[:1][0]['venue']

        # •	Top 4 teams in terms of wins
        top_4_query = Matches.objects.filter(season=season).values(
            'winner').annotate(wins=Count('winner')).order_by('-wins')[:4]
        top_4 = []
        for team in top_4_query:
            top_4.append(team['winner'])

        # •	Which player won the maximum number of Player of the Match awards in the whole season
        max_mom = Matches.objects.filter(season=season).values(
            'player_of_match').annotate(wins=Count('player_of_match')).order_by('-wins')[:1][0]['player_of_match']

        # •	Which location has the most number of wins for the top team
        max_hosted_venue_top_team = Matches.objects.filter(season=season, winner=won_max_mat).values(
            'venue').annotate(wins=Count('venue')).order_by('-venue')[:1][0]['venue']

        # •	Which % of teams decided to bat when they won the toss
        per_won_toss = round(len(Matches.objects.filter(season=season, toss_decision='bat'))
                             * 100/len(Matches.objects.filter(season=season)), 2)

        # •	How many times has a team won the toss and the match
        won_toss_match = len(Matches.objects.raw(
            "select id from matches where season="+str(season)+" and winner=toss_winner;"))

        filter_list = [x['id']
                       for x in Matches.objects.filter(season=season).values('id')]
        most_catches_query = list(Deliveries.objects.filter(match_id__in=filter_list).values('fielder', 'match_id').filter(
            Q(dismissal_kind='caught') | Q(dismissal_kind='caught and bowled')).annotate(catches=Count('fielder'),).order_by('-catches')[:1])
        most_catches = {
            'catches': most_catches_query[0]['catches'], 'player': most_catches_query[0]['fielder']}

        consolidated_data = {
            'highest_margin_run': highest_margin_run,
            'highest_margin_wickets': highest_margin_wickets,
            'most_tosses_won': most_tosses_won,
            'won_max_mat': won_max_mat,
            'max_hosted_venue': max_hosted_venue,
            'top_4': top_4,
            'max_mom': max_mom,
            'max_hosted_venue_top_team': max_hosted_venue_top_team,
            'per_won_toss': per_won_toss,
            'won_toss_match': won_toss_match,
            'most_catches': most_catches
        }
        # print (consolidated_data)
        return JsonResponse(consolidated_data)
    except Exception as e:
        return JsonResponse({'error': "Can't get the data: " + str(e)})


@api_view(['GET', 'POST'])
def charts(request):
    try:
        season = json.loads(request.body)['season']

        # matches won by each team
        matches_won_by_teams = []
        matches_won_by_teams_query = Matches.objects.filter(season=season).values(
            'winner').annotate(wins=Count('winner')).order_by('-winner')
        for team in matches_won_by_teams_query:
            matches_won_by_teams.append({
                'won': team['wins'],
                'team': team['winner']
            })

        # top wicket takers
        filter_list = Matches.objects.filter(season=season).values('id')
        bowlers = list(Deliveries.objects.filter(match_id__in=[x['id'] for x in filter_list]).values('bowler').filter(Q(dismissal_kind='caught') | Q(dismissal_kind='bowled') | Q(
            dismissal_kind='lbw') | Q(dismissal_kind='caught and bowled') | Q(dismissal_kind='stumped')).annotate(wickets=Count('bowler')).order_by('-wickets')[:10])

        # top run scorers
        runs = list(Deliveries.objects.filter(match_id__in=[x['id'] for x in filter_list]).values(
            'batsman').annotate(runs=Sum('batsman_runs')).order_by('-runs')[:10])

        chart_data = {
            'by_teams': matches_won_by_teams,
            'by_wickets': bowlers,
            'by_runs': runs
        }
        return JsonResponse(chart_data)
    except Exception as e:
        return JsonResponse({'error': "Can't get the data: " + str(e)})
