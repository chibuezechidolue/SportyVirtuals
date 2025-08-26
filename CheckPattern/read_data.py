# with open("../ScrapeData/data1.txt", "r") as file:
#     txt_file = file.readlines()

# for line in txt_file:
#     if line[2:11] == "League ID":
#         exec(f"new_season={line}")
#         won = False
#         a = {}
#         for league_id, league in new_season.items():
#             # Rotate the dictionary to start from week1 instead of week34
#             league = dict(list(league.items())[::-1])
#             for week, matches in league.items():
#                 a[league_id] = {}
#                 # a[league_id][week] = {1: None, 2: None, 3: None, }
#                 a[league_id][week] = {1: None, 2: None, 3: None, 4: None,
#                                       5: None, 6: None, 7: None, 8: None, 9: None}
#                 count = 1
#                 for teams, outcome in matches.items():
#                     ft_score = outcome['correct_score'][0]
#                     home_score = int(ft_score[0])
#                     away_score = int(ft_score[2])
#                     # if home_score > away_score or home_score < away_score:
#                     # if home_score == 0 or away_score == 0:
#                     if count > 0 and count < 4:
#                         if home_score+away_score < 3:
#                             # won = True
#                             a[league_id][week][count] = "won"
#                             # dic = a[league_id]
#                             # a[league_id] = dict(sorted(dic.items()))
#                     # if count > 2:
#                     #     break
#                     count += 1
#                 # print(week)
#                 if list(a[league_id][week].values()).count("won") == 3:
#                     won = True
#                     print(league_id, week, a[league_id][week])
#                     break
#             if won:
#                 break
#             else:
#                 print(f"{league_id}: failed")
#                 # print(a)
#                 a = {}

# uhdsihoi
# with open("../ScrapeData/data1.txt", "r") as file:
#     txt_file = file.readlines()

# for line in txt_file:
#     if line[2:11] == "League ID":
#         exec(f"new_season={line}")
#         won = False
#         for league_id, league in new_season.items():
#             for week, matches in league.items():
#                 for teams, outcome in matches.items():
#                     if outcome['correct_score'][0] == "3-3":
#                         # if outcome['ht/ft'][0] == "1/2" or outcome['ht/ft'][0] == "2/1":
#                         won = True
#                 if won:
#                     break
#             if won:
#                 print(f"{league_id}: won")
#                 break
#             else:
#                 print(f"{league_id}: failed")


with open("../ScrapeData/month1.txt", "r") as file:
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
                    if outcome["ht/ft"][0][:2] == "X/":
                        # won = True
                        a[league_id][week][count] = "won"
                        # dic = a[league_id]
                        # a[league_id] = dict(sorted(dic.items()))
                    # if count == 3:
                    #     break
                    count += 1
                # print(week)
                if not None in a[league_id][week].values():
                    # if list(a[league_id][week].values()).count("won") == 9:
                    won = True
                    week_won = week
                    break
            if won:
                with open("read_data_output.txt", "at") as file:
                    print(f"{league_id}: won | {week_won}", file=file)
                break
            else:
                with open("read_data_output.txt", "at") as file:
                    print(f"{league_id}: lost", file=file)
                # print(a)
                a = {}


# with open("../ScrapeData/data1.txt", "r") as file:
#     txt_file = file.readlines()

# for line in txt_file:
#     if line[2:11] == "League ID":
#         exec(f"new_season={line}")
#         won = False
#         a = {}
#         for league_id, league in new_season.items():
#             a[league_id] = {1: None, 2: None, 3: None, 4: None,
#                             5: None, 6: None, 7: None, 8: None, 9: None}
#             # Rotate the dictionary to start from week1 instead of week34
#             league = dict(list(league.items())[::-1])
#             for week, matches in league.items():
#                 if week == "Week 21":
#                     break
#                 count = 1
#                 for teams, outcome in matches.items():
#                     # if outcome['correct_score'][0] == "3-3":
#                     # if outcome['correct_score'][0] == "4-0" or outcome['correct_score'][0] == "0-4":
#                     # if outcome['correct_score'][0] == "4-1" or outcome['correct_score'][0] == "1-4":
#                     # if outcome['ht/ft'][0] == "1/2" or outcome['correct_score'][0] == "3-3":
#                     # if outcome['ht/ft'][0] == "2/1" or outcome['correct_score'][0] == "3-3":
#                     if outcome['ht/ft'][0] == "1/2" or outcome['ht/ft'][0] == "2/1":
#                         won = True
#                         a[league_id][count] = "won"
#                         # dic = a[league_id]
#                         # a[league_id] = dict(sorted(dic.items()))
#                     # if count == 11:
#                     #     break
#                     count += 1
#                 # print(week)
#                 if won:
#                     break
#             if won:
#                 print(f"{league_id}: won")
#                 break
#             else:
#                 # print(f"{league_id}: failed")
#                 print(a)
#                 a = {}
