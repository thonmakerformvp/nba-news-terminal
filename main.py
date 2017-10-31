import click
import json
import requests
import datetime


class NBAGame:
	def __init__(self, home_team, away_team, home_score, away_score, state):
		self.home_team = home_team
		self.away_team = away_team
		self.home_score = home_score
		self.away_score = away_score
		self.state = state

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
				final_games.append(NBAGame(home_team, away_team, game['h']['s'], game['v']['s'], game['stt']))
			elif len(game['stt'].split(" ")) == 3:
				pre_games.append(NBAGame(home_team, away_team, game['h']['s'], game['v']['s'], game['stt']))
			else:
				ongoing_games.append(NBAGame(home_team, away_team, game['h']['s'], game['v']['s'], game['stt']))
		
		if len(ongoing_games) > 0:
			print("ONGOING GAMES:")
			print("")
			for game in ongoing_games:
				print(("\t" + game.home_team + " VS " + game.away_team + "       " + str(game.home_score) + ":" + str(game.away_score) + "    " + game.state))
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

