with open("../ScrapeData/data/complete_data.txt", "r") as file:
    txt_file = file.readlines()

for line in txt_file:
    if line[2:11] == "League ID":
        exec(f"new_season={line}")
        won = False
        a = {}
        for league_id, league in new_season.items():
            a[league_id] = {}
            # Rotate the dictionary to start from week1 instead of week34
            league = dict(list(league.items())[::-1])
            for week, matches in league.items():
                a[league_id][week] = {
                    1: None,
                    2: None,
                    3: None,
                    4: None,
                    5: None,
                    6: None,
                    7: None,
                    8: None,
                    9: None,
                }
                # if week == "Week 21":
                #     break
                count = 1
                for teams, outcome in matches.items():
                    # if not "X/" in outcome['ht/ft'][0]:
                    h_score = outcome["correct_score"][0][0]
                    a_score = outcome["correct_score"][0][-1]
                    # print(h_score, a_score)
                    # if outcome["ht/ft"][0][:2] == "X/":
                    if int(h_score) + int(a_score) > 0:
                        # if int(h_score) < 1 or int(a_score) < 1:
                        # won = True
                        a[league_id][week][count] = "won"
                        # dic = a[league_id]
                        # a[league_id] = dict(sorted(dic.items()))
                    # if count == 3:
                    #     break
                    count += 1
                # print(week)
                # if not None in a[league_id][week].values():
                if list(a[league_id][week].values()).count("won") == 9:
                    won = True
                    week_won = week
                    break
            if won:
                with open("read_data_output.txt", "at") as file:
                    print(f"{league_id}: won | {week_won}", file=file)
                # break
            else:
                with open("read_data_output.txt", "at") as file:
                    print(f"{league_id}: lost", file=file)
                # print(a)
                a = {}
