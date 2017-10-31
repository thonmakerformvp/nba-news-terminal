import click
import json
import requests
import datetime

def draw_lead_tracker(date, game_id):
	q1_url = "https://data.nba.net/data/10s/prod/v1/" + date + "/" + game_id + '_lead_tracker_1.json'
	q1_r = requests.get(q1_url)
	q1_d = json.loads(q1_r.content)

	q2_url = "https://data.nba.net/data/10s/prod/v1/" + date + "/" + game_id + '_lead_tracker_2.json'
	q2_r = requests.get(q2_url)
	q2_d = json.loads(q2_r.content)

	q3_url = "https://data.nba.net/data/10s/prod/v1/" + date + "/" + game_id + '_lead_tracker_3.json'
	q3_r = requests.get(q3_url)
	q3_d = json.loads(q3_r.content)

	q4_url = "https://data.nba.net/data/10s/prod/v1/" + date + "/" + game_id + '_lead_tracker_4.json'
	q4_r = requests.get(q4_url)
	q4_d = json.loads(q4_r.content)

	all_plays = q1_d['plays'] + q2_d['plays'] + q3_d['plays'] + q4_d['plays']

	max_lead = 0
	for play in all_plays:
		if int(play['points']) > max_lead:
			max_lead = int(play['points'])

	height_of_chart = 36

	top_team_id = all_plays[0]['leadTeamId']

	for iii in range(0, height_of_chart):
		for play in all_plays:
			if play['leadTeamId'] == top_team_id and iii <= (height_of_chart/2):
				height_of_lead_this_play_in_lines = (int(play['points']) / max_lead) * (height_of_chart / 2)
				if height_of_chart / 2 - iii < height_of_lead_this_play_in_lines:
					print("#", end="")
				else:
					print(" ", end="")
			elif play['leadTeamId'] != top_team_id and iii > (height_of_chart/2):
				height_of_lead_this_play_in_lines = (float(play['points']) / float(max_lead)) * float((height_of_chart / 2))
				if iii - (height_of_chart/2) < height_of_lead_this_play_in_lines:
					print("#", end="")
				else:
					print(" ", end="")
			else:
				print(" ", end="")
			'''else:
				print("YOU FCUKED UP U FUCKING IDIOT")
				print(iii)
				print(type(iii))
				print(type(height_of_chart/2))
				print(height_of_chart/2)
				print(play['leadTeamId'])
				print(top_team_id)
				print(type(play['leadTeamId']))
				print(type(top_team_id))
				print('------')'''
		if iii == height_of_chart / 2:
			print("")
			last_time = 20
			quarter = 1
			skip_next = False
			for play in all_plays:
				if int(play['clock'].split(':')[0]) > last_time:
					quarter = quarter + 1
					print('Q' + str(quarter), end='')
					skip_next = True
				else:
					if skip_next == True:
						skip_next = False
					else:
						print('-', end='')
				last_time = int(play['clock'].split(':')[0])
			print('')
		else:
			print("")


class NBAGame:
	def __init__(self, home_team, away_team, home_score, away_score, state, home_team_top_scorer="", home_team_top_assister="", home_team_top_rebounder="", away_team_top_scorer="", away_team_top_assister="", away_team_top_rebounder=""):
		self.home_team = home_team
		self.away_team = away_team
		self.home_score = home_score
		self.away_score = away_score
		self.state = state

		self.home_team_top_scorer = home_team_top_scorer
		self.home_team_top_assister = home_team_top_assister
		self.home_team_top_rebounder = home_team_top_rebounder

		self.away_team_top_scorer = away_team_top_scorer
		self.away_team_top_assister = away_team_top_assister
		self.away_team_top_rebounder = away_team_top_rebounder

#For full NBA schedule: http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/league/00_full_schedule_week.json


@click.command()
@click.option('--lookup', default="games", help='Number of greetings.')
@click.option('--name')

def main_method(lookup, name):
	if lookup == 'games':
		print("")

		final_games = []
		ongoing_games = []
		pre_games = []


		url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/scores/00_todays_scores.json"
		r = requests.get(url)
		d = json.loads(r.content)

		for game in d['gs']['g']:
			#print(game['h'])
			home_team = game['h']['ta'] + " " + game['h']['tn']
			away_team = game['v']['tn'] + " " + game['v']['ta']
			final_score = str(game['h']['s']) + " : " + str(game['v']['s'])
			#print(home_team + " VS " + away_team + "       " + final_score)
			if game['stt'] == 'Final':
				score_leaders_url = "http://stats.nba.com/js/data/widgets/scores_leaders.json"
				r_score_leaders = requests.get(score_leaders_url)
				d_score_leaders = json.loads(r_score_leaders.content)

				game_object = NBAGame(home_team, away_team, game['h']['s'], game['v']['s'], game['stt'])
				for game_stats in d_score_leaders['items'][0]['items'][0]['playergametats']:
					if game_stats['GAME_ID'] == game['gid'] and game_stats['TEAM_ABBREVIATION'] == game['h']['ta']:
						game_object.home_team_top_scorer = game_stats['PTS_PLAYER_NAME'] + "::" + str(game_stats['PTS'])
						game_object.home_team_top_rebounder = game_stats['REB_PLAYER_NAME'] + "::" + str(game_stats['REB'])
						game_object.home_team_top_assister = game_stats['AST_PLAYER_NAME'] + "::" + str(game_stats['AST'])
					elif game_stats['GAME_ID'] == game['gid'] and game_stats['TEAM_ABBREVIATION'] == game['v']['ta']:
						game_object.away_team_top_scorer = game_stats['PTS_PLAYER_NAME'] + "::" + str(game_stats['PTS'])
						game_object.away_team_top_rebounder = game_stats['REB_PLAYER_NAME'] + "::" + str(game_stats['REB'])
						game_object.away_team_top_assister = game_stats['AST_PLAYER_NAME'] + "::" + str(game_stats['AST'])
				
				final_games.append(game_object)
			elif len(game['stt'].split(" ")) == 3:
				pre_games.append(NBAGame(home_team, away_team, game['h']['s'], game['v']['s'], game['stt']))
			else:
				score_leaders_url = "http://stats.nba.com/js/data/widgets/scores_leaders.json"
				r_score_leaders = requests.get(score_leaders_url)
				d_score_leaders = json.loads(r_score_leaders.content)

				game_object = NBAGame(home_team, away_team, game['h']['s'], game['v']['s'], game['stt'])
				for game_stats in d_score_leaders['items'][0]['items'][0]['playergametats']:
					if game_stats['GAME_ID'] == game['gid'] and game_stats['TEAM_ABBREVIATION'] == game['h']['ta']:
						game_object.home_team_top_scorer = game_stats['PTS_PLAYER_NAME'] + ": " + str(game_stats['PTS'])
						game_object.home_team_top_rebounder = game_stats['REB_PLAYER_NAME'] + ": " + str(game_stats['REB'])
						game_object.home_team_top_assister = game_stats['AST_PLAYER_NAME'] + ": " + str(game_stats['AST'])
					elif game_stats['GAME_ID'] == game['gid'] and game_stats['TEAM_ABBREVIATION'] == game['v']['ta']:
						game_object.away_team_top_scorer = game_stats['PTS_PLAYER_NAME'] + ": " + str(game_stats['PTS'])
						game_object.away_team_top_rebounder = game_stats['REB_PLAYER_NAME'] + ": " + str(game_stats['REB'])
						game_object.away_team_top_assister = game_stats['AST_PLAYER_NAME'] + ": " + str(game_stats['AST'])
				
				ongoing_games.append(game_object)
		
		if len(ongoing_games) > 0:
			print("ONGOING GAMES:")
			print("")
			for game in ongoing_games:
				print(("\t" + game.home_team + " VS " + game.away_team + "       " + str(game.home_score) + ":" + str(game.away_score) + "    " + game.state))
				print("\t\t" + game.home_team_top_scorer + " PTS, " + game.away_team_top_scorer + " PTS")
				print("\t\t" + game.home_team_top_rebounder + " REBS, " + game.away_team_top_rebounder + " REBS")
				print("\t\t" + game.home_team_top_assister + " ASTS, " + game.away_team_top_assister + " ASTS")
				print("")
			print("")

		if len(final_games) > 0:
			print("FINAL GAMES:")
			print("")
			for game in final_games:
				print(("\t" + game.home_team + " VS " + game.away_team + "       " + str(game.home_score) + ":" + str(game.away_score)))
				print("")

		if len(pre_games) > 0:
			print("UPCOMING GAMES TODAY:")
			print("")
			for game in pre_games:
				print(("\t" + game.home_team + " VS " + game.away_team + "       " + str(game.state)))
				print("")
			print("")

		print("")
	elif lookup == 'game-summary':
		print("")
		current_date = datetime.datetime.now()
		url = "http://stats.nba.com/js/data/widgets/boxscore_breakdown_" + current_date.strftime("%Y%m%d") + ".json"
		r = requests.get(url)
		d = json.loads(r.content)

		for breakdown in d['results']:
			if breakdown['Breakdown'] != '':
				print(breakdown['Game'])
				print(breakdown['Breakdown'])
				print('')
				print('')
				print('')
	elif lookup == 'print-lead-summary':
		draw_lead_tracker('20171030', '0021700100')
	'''elif lookup.split(" ")[0] == 'boxscore':
		print("GRRR")
		home_team_symbol = lookup.split(" ")[1].split(":")[0]
		away_team_symbol = lookup.split(-" ")[1].split(":")[1]

		url = "https://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2017/scores/00_todays_scores.json"
		r = requests.get(url)
		d = json.loads(r.content)
		print("BARK")
		for game in d['gs']['g']:
			print("OINK")
			home_team = game['h']['ta'] 
			away_team = game['v']['ta']
			if (home_team_symbol.upper() == home_team or home_team_symbol.upper() == away_team) and (away_team_symbol.upper() == home_team or away_team_symbol.upper() == away_team):
				print("HEREEEE")
				game_id = game['gid']
				print(game_id)
				url2 = "http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=" + game_id + "&RangeType=0&Season=2017-18&SeasonType=Regular+Season&StartPeriod=1&StartRange=0"
				print('hissss')
				r2 = requests.get(url2)
				print('ohhh')
				d2 = json.loads(r2.content)
				print(d2)'''

if __name__ == '__main__':
	main_method()





