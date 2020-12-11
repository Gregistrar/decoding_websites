import requests
from requests import get
import pandas as pd
import itertools
import re
import numpy as np
import matplotlib.pyplot as plt


pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

season = 2020
weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
league_id = '601091358869999616'
base_url = 'https://api.sleeper.app/v1/'
league_url = base_url + 'league/' + str(league_id) + '/'
users = ['gregistrar', 'phranc26', 'the1commish', 'markgordon', 'brenner1212',
         'mlinkens', 'greenemachine88', 'elprofe', 'augo', 'champman']
save_folder = 'C:/Users/ghodg/Desktop/'

# Get Roster data for each team
a = requests.get('https://api.sleeper.app/v1/league/601091358869999616/rosters')
j = a.json()
roster_df = pd.DataFrame.from_dict(j)
roster_df.columns
roster_df.to_clipboard()

roster_df['record'] = [d.get('record') for d in roster_df.metadata]
roster_df['wins'] = roster_df['record'].str.count('W')
roster_df['losses'] = roster_df['record'].str.count('L')


def win_streak(team):
    a = len(max(re.findall(r'(?:W)+', team), key=len))
    return a


def loss_streak(team):
    a = len(max(re.findall(r'(?:L)+', team), key=len))
    return a


roster_df['max_win_streak'] = roster_df['record'].apply(win_streak)
roster_df['max_loss_streak'] = roster_df['record'].apply(loss_streak)
roster_df['win_pct'] = roster_df['wins'] / (roster_df['wins'] + roster_df['losses'])
roster_df['lose_pct'] = roster_df['losses'] / (roster_df['wins'] + roster_df['losses'])

roster_df_fin = roster_df[['league_id', 'owner_id', 'roster_id', 'record', 'wins', 'losses', 'max_win_streak',
                           'max_loss_streak', 'win_pct', 'lose_pct', 'starters', 'reserve', 'players',]]
roster_df_fin.to_clipboard()


# Get User data
user_data = []
for user in users:
    id_user = requests.get('https://api.sleeper.app/v1/user/{}'.format(user))
    x = id_user.json()
    user_data.append(x)

user_data[0]
user_df = pd.DataFrame.from_dict(user_data)
user_df = user_df[['user_id', 'username', 'display_name']].copy()

final_roster = pd.merge(roster_df_fin, user_df, how='left', left_on='owner_id', right_on='user_id')
cols = list(final_roster)
cols.insert(2, cols.pop(cols.index('username')))
cols.insert(3, cols.pop(cols.index('display_name')))

final_roster = final_roster[cols]
final_roster.to_clipboard(index=False)

# Add team name
tm = get('https://api.sleeper.app/v1/league/{}/users'.format(league_id))
tms = tm.json()
team_names = pd.DataFrame.from_dict(tms)
team_names['team_name'] = [d.get('team_name') for d in team_names.metadata]
team_names['team_name'] = team_names['team_name'].fillna(value='The Commish')

final_roster = pd.merge(final_roster, team_names[['user_id', 'team_name']], how='left', left_on='owner_id', right_on='user_id')
cols = list(final_roster)
cols.insert(4, cols.pop(cols.index('team_name')))
final_roster = final_roster[cols]
final_roster.drop(['user_id_x', 'user_id_y'], inplace=True, axis=1)
final_roster.to_clipboard(index=False)


# Get League matchups
all_matchups = []
all_matchups_plus = []
for i in weeks:
    matches = get(league_url + '/matchups/' + str(i)).json()
    all_matchups.append(matches)
    z = pd.DataFrame.from_dict(matches)
    z['week'] = i
    all_matchups_plus.append(z)


team_points_weekly = final_roster[['owner_id', 'roster_id', 'username']]
for i in all_matchups_plus:
    pts = i[['roster_id', 'points']]
    pts.rename(columns={'points': 'week_{}'.format(i['week'][0])}, inplace=True)
    team_points_weekly = pd.merge(team_points_weekly, pts, how='left', on='roster_id')


# Making Graphs
test_graph_df = team_points_weekly.drop(['owner_id', 'roster_id'], axis=1).set_index('username').transpose().reset_index()
plt.style.use('seaborn-darkgrid')
# plt.style.use('seaborn-notebook')
palette = plt.get_cmap('Set1')

# Subplot each team only
num = 0
for column in test_graph_df.drop(['index'], axis=1):
    num += 1

    # Find the right spot on the plot
    plt.subplot(5, 2, num)
    plt.tight_layout()

    # Plot the lineplot
    plt.plot(test_graph_df['index'], test_graph_df[column], marker='',
             color=palette(num), linewidth=1.9, alpha=0.9, label=column)

    # Same limits for everybody!
    plt.xlim(0, 12)
    plt.ylim(60, 180)

    # Add title
    plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num))

plt.savefig(save_folder + 'ff_all_week_scoring.png', dpi=800)

# Subplot each team with others in background
num = 0
for column in test_graph_df.drop(['index'], axis=1):
    num += 1

    # Find the right spot on the plot
    ax1 = plt.subplot(5, 2, num)
    # plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)

    # plot every groups, but discreet
    for v in test_graph_df.drop('index', axis=1):
        ax1.plot(test_graph_df['index'], test_graph_df[v], marker='', color='grey', linewidth=0.6, alpha=0.3)

    # Plot the lineplot
    ax1.plot(test_graph_df['index'], test_graph_df[column], marker='',
             color=palette(num), linewidth=1.9, alpha=0.9, label=column)

    # Annotate highest score
    x = list(test_graph_df['index'])
    y = list(test_graph_df[column])
    ymax = max(y)
    xpos = y.index(ymax)
    xmax = x[xpos]
    ax1.annotate(ymax, xy=(xmax, ymax), xytext=(xmax, ymax+5), fontsize=12)

    # Annotate lowest score
    x = list(test_graph_df['index'])
    y = list(test_graph_df[column])
    ymin = min(y)
    xpos1 = y.index(ymin)
    xmin = x[xpos1]
    ax1.annotate(ymin, xy=(xmin, ymin), xytext=(xmin, ymin - 15), fontsize=12)

    # Same limits for everybody!
    plt.xlim(0, 12)
    plt.ylim(60, 180)

    # Add title
    plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num))

# general title
plt.suptitle("2020 Weekly Scoring Comparison", fontsize=28, fontweight='bold', color='black', style='italic')
# Axis title
plt.text(-1, 0, 'Week', ha='center', va='center')
plt.text(-15.4, 500, 'Score', ha='center', va='center', rotation='vertical')

plt.savefig(save_folder + 'ff_all_week_scoring_plus1.jpg', dpi=800)


# Matchup data
pd.DataFrame.from_dict(all_matchups[0]).to_clipboard()
pd.DataFrame.from_dict(all_matchups_plus[0]).to_clipboard()








all_matchup_pairs = []
for x in all_matchups:
    matchup_pairs = {}
    for matchup in x:
        matchup_id = matchup['matchup_id']
        roster_id = matchup['roster_id']
        if matchup_id in matchup_pairs:
            matchup_pairs[matchup_id] = [roster_id, matchup_pairs[matchup_id]]
        else:
            matchup_pairs[matchup_id] = roster_id
    all_matchup_pairs.append({'week_{}'.format(): matchup_pairs})

{'week_1': matchup_pairs}

all_matchups_plus[0]
z.to_clipboard()



league = requests.get('https://api.sleeper.app/v1/league/{}/matchups/13'.format(league_id))
league_matchups = league.json()
league_matchups[2]
a[0]
len(league_matchups)








players = requests.get(base_url + 'players/nfl').json()
players_df = pd.DataFrame.from_dict(players, orient='index')
players_df.info()
players_df.head()
players_df.to_clipboard()

stats = requests.get(base_url + 'stats/nfl/regular/' + str(season) + '/' + str(1)).json()
stats_df = pd.DataFrame.from_dict(stats, orient='index')

rosters = get(league_url + 'rosters').json()
users = get(league_url + 'users').json()
roster_dict = {x['owner_id']:x['roster_id'] for x in rosters}
user_dict = {x['user_id']:x['display_name'] for x in users}
teams = {roster_id:user_dict[user] for user, roster_id in roster_dict.items()}

matchups = get(league_url + '/matchups/' + str(1)).json()
matchup_pairs = {}
for matchup in matchups:
    matchup_id = matchup['matchup_id']
    roster_id = matchup['roster_id']
    if matchup_id in matchup_pairs:
        matchup_pairs[matchup_id] = [roster_id, matchup_pairs[matchup_id]]
    else:
        matchup_pairs[matchup_id] = roster_id

# teams = getTeams()
players = {}
#matchup_pairs = getMatchupPairs(matchups)
for matchup in matchups:
    matchup_id = matchup['matchup_id']
    matchup_pair = matchup_pairs[matchup_id]
    roster_id = matchup['roster_id']
    opponent_id = [x for x in matchup_pair if x != roster_id][0]
    for player in matchup['players']:
        players[player] = {
            'matchup_id':matchup_id,
            'team_name':teams[roster_id],
            'opponent_name':teams[opponent_id],
            'is_starter':True if player in matchup['starters'] else False}
fin = pd.DataFrame.from_dict(players, orient='index')
fin.to_clipboard()





