
"League ID 4697"


b = {'League ID 4856': {'Week 30': {'LEV - UBE': {'correct_score': ['2-0', '7.58'], 'ht/ft': ['1/1', '1.89']}, 'HOF - FRE': {'correct_score': ['3-0', '22.7'], 'ht/ft': ['1/1', '3.24']}, 'MNZ - HDH': {'correct_score': ['2-2', '14.8'], 'ht/ft': ['X/X', '5.02']}, 'AUG - BOC': {'correct_score': ['3-1', '21.9'], 'ht/ft': ['X/1', '6.07']}, 'WLF - FRA': {
    'correct_score': ['2-2', '15.3'], 'ht/ft': ['X/X', '5.05']}, 'STP - BMU': {'correct_score': ['1-5', '49.2'], 'ht/ft': ['2/2', '2.02']}, 'STU - BRE': {'correct_score': ['0-1', '14.9'], 'ht/ft': ['2/2', '7.54']}, 'RBL - BVB': {'correct_score': ['3-3', '51.7'], 'ht/ft': ['1/X', '16.5']}, 'KIE - MGB': {'correct_score': ['2-1', '13.9'], 'ht/ft': ['X/1', '8.02']}}}}
for league in b.values():
    for week, matches in league.items():
        for teams, outcome in matches.items():
            print(outcome['correct_score'][0])
            if outcome['correct_score'][0] == "2-0":
                print('won')
                break
