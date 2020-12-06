"""Koden er udviklet af:
    Navn: Kent Vugs Nielsen
    email: kniels18@student.aau.dk
    Gruppe: A308b
    Programmet er udviklet selvstændigt og individuelt.
"""

import os
import pandas as pd

"""Global variables - path to files"""
nations_file = "data/nations.txt"
result_file = "data/results.csv"
round_files = ["data/round1.txt", "data/round2.txt", "data/round3.txt"]


def get_nations():
    """Return nations from nation file"""
    with open(nations_file, "r") as f:
        nation = f.read()
    nations = nation.rstrip().split("\n")
    return nations


def get_scores():
    """Load current scores"""
    if os.path.isfile(result_file):
        df = pd.read_csv(result_file, index_col=0).sort_values("PTS", ascending=False)
    else:
        nations_dict = dict.fromkeys(get_nations(), {"M": 0, "W": 0, "D": 0, "L": 0, "G+": 0,
                                                     "G-": 0, "GD": 0, "PTS": 0})
        _save_current_score_to_file(nations_dict)
        df = get_scores()

    return df


def _save_current_score_to_file(df_dict):
    """Save score to file"""
    df = pd.DataFrame.from_dict(df_dict, orient='index')
    df.to_csv(result_file)


def get_matches(match_files):
    """return matches played from file/(s)"""
    all_matches = []
    if isinstance(match_files, list):
        for match in match_files:
            with open(match, "r") as f:
                round_matches = f.read()
            all_matches.extend(round_matches.rstrip().split("\n"))
    elif isinstance(match_files, str):
        with open(match_files, "r") as f:
            round_matches = f.read()
        all_matches.extend(round_matches.rstrip().split("\n"))

    return all_matches


def get_winner_teams(matches):
    """return the winner teams from the played matches."""
    winners = []
    for match in matches:
        goals_scored = _get_team_score(match, "s")
        if goals_scored[0] > goals_scored[1]:
            winners.append(_get_team_score(match, 't')[0])
        elif goals_scored[0] < goals_scored[1]:
            winners.append(_get_team_score(match, 't')[1])
        else:
            winners.append(_get_team_score(match, 't'))
    return winners


def _get_team_score(match, team_score):
    """return the teams or scores from a match"""
    if team_score == "t":
        team = match.split()[:3]
        team.pop(1)
        return team
    elif team_score == "s":
        score = match.split()[-3:]
        score.pop(1)
        for s in range(len(score)):
            score[s] = int(score[s])
        return score


def update_scores(matches):
    """Updates the scores from matches played"""
    for match in matches:
        competing_teams = match.split()[:3]
        competing_teams.pop(1)
        game_score = match.split()[-3:]
        game_score.pop(1)
        game_score = [int(s) for s in game_score]
        for team in competing_teams:
            if team in scores_dict:
                scores_dict[team]["M"] += 1
            if game_score[0] > game_score[1]:
                if team == competing_teams[0]:
                    scores_dict[team]["W"] += 1
                    scores_dict[team]["G+"] += game_score[0]
                    scores_dict[team]["G-"] += game_score[1]
                    scores_dict[team]["GD"] += (game_score[0] - game_score[1])
                    scores_dict[team]["PTS"] += 3
                else:
                    scores_dict[team]["L"] += 1
                    scores_dict[team]["G+"] += game_score[1]
                    scores_dict[team]["G-"] += game_score[0]
                    scores_dict[team]["GD"] += (game_score[1] - game_score[0])
                    scores_dict[team]["PTS"] += 0

            elif game_score[0] < game_score[1]:
                if team == competing_teams[1]:
                    scores_dict[team]["W"] += 1
                    scores_dict[team]["G+"] += game_score[1]
                    scores_dict[team]["G-"] += game_score[0]
                    scores_dict[team]["GD"] += (game_score[1] - game_score[0])
                    scores_dict[team]["PTS"] += 3
                else:
                    scores_dict[team]["L"] += 1
                    scores_dict[team]["G+"] += game_score[0]
                    scores_dict[team]["G-"] += game_score[1]
                    scores_dict[team]["GD"] += (game_score[0] - game_score[1])
                    scores_dict[team]["PTS"] += 0
            else:
                if team == competing_teams[0]:
                    scores_dict[team]["D"] += 1
                    scores_dict[team]["G+"] += game_score[0]
                    scores_dict[team]["G-"] += game_score[1]
                    scores_dict[team]["GD"] += (game_score[0] - game_score[1])
                    scores_dict[team]["PTS"] += 1
                else:
                    scores_dict[team]["D"] += 1
                    scores_dict[team]["G+"] += game_score[1]
                    scores_dict[team]["G-"] += game_score[0]
                    scores_dict[team]["GD"] += (game_score[1] - game_score[0])
                    scores_dict[team]["PTS"] += 1

    _save_current_score_to_file(scores_dict)


"""Main code"""
current_scores = get_scores()
print(f"Scores on Load:\n{current_scores}")
scores_dict = current_scores.to_dict('index')
update_scores(get_matches(round_files))
print(f"Updated scores:\n{get_scores()}")
