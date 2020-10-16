import os

nations_file = "data/nations.txt"
result_file = "data/result.txt"
round_files = ["data/round1.txt", "data/round2.txt", "data/round3.txt"]
results_list = [0, 0, 0, 0]


def get_nations():
    with open(nations_file, "r") as f:
        nation = f.read()
    nations = nation.rstrip().split("\n")
    return nations


def cr_result_file(nations):
    if os.path.isfile("data/result.txt"):
        with open(result_file, "r") as f:
            result = f.read()
        results = result.split("\n")
        for i, r in enumerate(results):
            results_list[i] = int(r.split()[1])
    else:
        _save_current_score_to_file(nations)


def _save_current_score_to_file(teams):
    with open(result_file, "w") as f:
        for i, team in enumerate(teams):
            if len(teams) == i + 1:
                f.write(f"{team}: {results_list[i]}")
            else:
                f.write(f"{team}: {results_list[i]}\n")


def get_matches(match_files):
    all_matches = []
    if isinstance(match_files, list):
        for match in match_files:
            with open(match, "r") as f:
                round_matches = f.read()
            round_matches = round_matches.rstrip().split("\n")
            for r in round_matches:
                all_matches.append(r)
    elif isinstance(match_files, str):
        with open(match_files, "r") as f:
            round_matches = f.read()
        round_matches = round_matches.rstrip().split("\n")
        for r in round_matches:
            all_matches.append(r)

    return all_matches


def get_winner_teams(matches):
    winners = []
    for match in matches:
        if _get_team_score(match, "s")[0] > _get_team_score(match, "s")[1]:
            winners.append(_get_team_score(match, 't')[0])
        elif _get_team_score(match, "s")[0] < _get_team_score(match, "s")[1]:
            winners.append(_get_team_score(match, 't')[1])
        else:
            winners.append(_get_team_score(match, 't'))
    return winners


def _get_team_score(match, team_score):
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


def update_score(matches):
    winners = get_winner_teams(get_matches(matches))
    teams = get_nations()
    for winner in winners:
        if winner in teams:
            for i in range(len(teams)):
                if winner == teams[i]:
                    results_list[i] += 3
        else:
            if isinstance(winner, list):
                for r in winner:
                    for i in range(len(teams)):
                        if r == teams[i]:
                            results_list[i] += 1
    _save_current_score_to_file(teams)


cr_result_file(get_nations())
update_score(round_files)

