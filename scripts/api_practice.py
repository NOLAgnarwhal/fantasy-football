import sys

try:
    import requests
except ImportError:
    sys.exit('requests was not properly installed. Try again. Are you sure you are in a venv?')

def get_fantasy_points(player, pos):
    if player.get('position') == pos:
        return player.get('fantasy_points').get('ppr')

pos = 'WR'
year = '2019'
week = 1

res = requests.get('https://www.fantasyfootballdatapros.com/api/players/{0}/{1}'.format(year, week))

if res.ok:
    print('Season {0}, week {1} VOR for {2}s'.format(year, week, pos))
    print('-'*40)

    data = res.json()

    wr_fantasy_points = [get_fantasy_points(player, pos) for player in data]

    wr_fantasy_points = list(filter(lambda x: x is not None, wr_fantasy_points))

    mean = lambda x: sum(x)/len(x)

    replacement_value = mean(wr_fantasy_points)

    for player in data:
        if player.get('position') == pos:
            vor = player.get('fantasy_points').get('ppr') - replacement_value
            print(
                player.get('player_name'), 'had a VOR of', vor
            )