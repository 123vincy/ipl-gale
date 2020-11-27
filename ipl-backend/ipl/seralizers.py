import serpy


class MatchesSerializer(serpy.Serializer):
    id = serpy.Field()
    season = serpy.Field()
    city = serpy.Field()
    date = serpy.Field()
    team1 = serpy.Field()
    team2 = serpy.Field()
    toss_winner = serpy.Field()
    toss_decision = serpy.Field()
    result = serpy.Field()
    dl_applied = serpy.Field()
    winner = serpy.Field()
    win_by_runs = serpy.Field()
    win_by_wickets = serpy.Field()
    player_of_match = serpy.Field()
    venue = serpy.Field()
    umpire1 = serpy.Field()
    umpire2 = serpy.Field()
    umpire3 = serpy.Field()
    extra = serpy.Field()
