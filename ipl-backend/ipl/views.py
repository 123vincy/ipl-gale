from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
import json

# using pandas for computing statistics
import numpy as np
import pandas as pd

data_path = os.path.join(os.path.dirname(__file__), 'data/')


@api_view(['GET', 'POST'])
def seasons(request):
    try:
        df = pd.read_csv(data_path+'matches.csv', encoding='utf-8')
        df = df.replace({np.nan: None})

        unique_seasons = df['season'].unique().tolist()
        unique_seasons.sort(reverse=True)
        return JsonResponse({'seasons': unique_seasons})
    except Exception as e:
        return JsonResponse({'error': "Can't get the data: " + str(e)})


@api_view(['GET', 'POST'])
def statistics(request):
    try:
        season = json.loads(request.body)['season']
        df = pd.read_csv(data_path+'matches.csv', encoding='utf-8')
        df = df.replace({np.nan: None})

        # filtering for the selected season
        df = df[df['season'] == season].reset_index()

        # •	Which team won by the highest margin of runs  for the season
        highest_margin_run = df.iloc[df['win_by_runs'].idxmax()]['winner']

        # •	Which team won by the highest number of wickets for the season
        highest_margin_wickets = df.iloc[df['win_by_wickets'].idxmax(
        )]['winner']

        # •	Which team won the most number of tosses in the season
        most_tosses_won = df.toss_winner.value_counts().keys()[0]

        # • Which team won max matches in the whole season
        won_max_mat = df.winner.value_counts().keys()[0]

        # •	Which location hosted most number of matches
        max_hosted_venue = df.venue.value_counts().keys()[0]

        # •	Top 4 teams in terms of wins
        top_4 = df.winner.value_counts().keys()[0:4].tolist()

        # •	Which player won the maximum number of Player of the Match awards in the whole season
        max_mom = df.player_of_match.value_counts().keys()[0]

        # •	Which location has the most number of wins for the top team
        max_hosted_venue_top_team = df[df['winner'] ==
                                       won_max_mat].venue.value_counts().keys()[0]

        # •	Which % of teams decided to bat when they won the toss
        per_won_toss = round((df['toss_decision'].value_counts()
                              ['bat'] * 100) / len(df), 2)

        # •	How many times has a team won the toss and the match
        won_toss_match = len(df[df['winner'] == df['toss_winner']])

        '--------------------------------------------------------------------------'

        df_del = pd.read_csv(data_path+'deliveries.csv', encoding='utf-8')
        df_del = df_del.replace({np.nan: None})

        # to filter the deliveries.csv we have to get the ids of the mathces
        ids = df[df['season'] == season]['id'].tolist()

        # filtering for the seected season and dismissal by catch
        df_del = df_del[df_del['player_dismissed'].notna() &
                        df_del['match_id'].isin(ids) &
                        ((df_del['dismissal_kind'] == 'caught') | (df_del['dismissal_kind'] == 'caught and bowled'))].reset_index()

        groups = df_del.groupby('match_id')
        most_catches = {
            'catches': 0,
            'player': ''
        }

        # grouping for each match and finding the player taking most number of catches
        for name, group in groups:
            max_cat = group.fielder.value_counts()
            if (max_cat[0] > most_catches['catches']):
                most_catches['catches'] = int(max_cat[0])
                most_catches['player'] = max_cat.keys()[0]

        consolidated_data = {
            'highest_margin_run': highest_margin_run,
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
        df = pd.read_csv(data_path+'matches.csv', encoding='utf-8')
        df = df.replace({np.nan: None})

        # filtering for the selected season
        df = df[df['season'] == season].reset_index()
        df_del = pd.read_csv(data_path+'deliveries.csv', encoding='utf-8')
        df_del = df_del.replace({np.nan: None})

        # to filter the deliveries.csv we have to get the ids of the mathces
        ids = df[df['season'] == season]['id'].tolist()
        # filtering for the seected season and dismissal by catch
        df_del = df_del[df_del['match_id'].isin(ids)].reset_index()

        # matches won by each team
        matches_won_by_teams = []
        for team, count in df.winner.value_counts().iteritems():
            matches_won_by_teams.append({
                'won': count,
                'team': team
            })

        # top wicket takers
        wickets = []
        bowlers = df_del[['bowler', 'dismissal_kind']]
        bowlers = bowlers[(bowlers.dismissal_kind.isin(
            ['caught', 'bowled', 'lbw', 'caught and bowled', 'stumped']))]
        bowlers = bowlers.groupby('bowler').count().reset_index()
        bowlers = bowlers.sort_values(
            by='dismissal_kind', ascending=False).head(10)
        for index, row in bowlers.iterrows():
            wickets.append({
                'wickets': row['dismissal_kind'],
                'bowler': row['bowler']
            })

        # top run scorers
        runs = []
        batsman = df_del[['batsman', 'batsman_runs']]
        batsman = batsman.groupby(
            'batsman')['batsman_runs'].sum().reset_index()
        batsman = batsman.sort_values(
            by='batsman_runs', ascending=False).head(10)
        for index, row in batsman.iterrows():
            runs.append({
                'runs': row['batsman_runs'],
                'batsman': row['batsman']
            })

        chart_data = {
            'by_teams': matches_won_by_teams,
            'by_wickets': wickets,
            'by_runs': runs
        }
        return JsonResponse(chart_data)
    except Exception as e:
        return JsonResponse({'error': "Can't get the data: " + str(e)})
