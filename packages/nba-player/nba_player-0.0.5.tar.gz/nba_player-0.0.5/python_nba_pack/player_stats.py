# this file will get player offensive statistics
import json
import time
import datetime
from requests_futures.sessions import FuturesSession
from .NBAObjects import NBAObjects
import requests
from bs4 import BeautifulSoup
from lxml import html

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

all_player_params = (
    ('LeagueID', '00'),
    ('Season', '2016-17'),
    ('IsOnlyCurrentSeason', '0'),
)

def retStuff(year, str):
    return (
        ('College', ''),
        ('Conference', ''),
        ('Country', ''),
        ('DateFrom', ''),
        ('DateTo', ''),
        ('Division', ''),
        ('DraftPick', ''),
        ('DraftYear', ''),
        ('GameScope', ''),
        ('Height', ''),
        ('LastNGames', '0'),
        ('LeagueID', '00'),
        ('Location', ''),
        ('Month', '0'),
        ('OpponentTeamID', '0'),
        ('Outcome', ''),
        ('PORound', '0'),
        ('PerMode', 'PerGame'),
        ('PlayerExperience', ''),
        ('PlayerOrTeam', 'Player'),
        ('PlayerPosition', ''),
        ('PtMeasureType', str),
        ('Season', year),
        ('SeasonSegment', ''),
        ('SeasonType', 'Regular Season'),
        ('StarterBench', ''),
        ('TeamID', '0'),
        ('VsConference', ''),
        ('VsDivision', ''),
        ('Weight', '')
    )

def contract_return(player_contract, year_object, information, year_string):
    year_object = information.text
    if information["class"][1] == "salary-tm":
        player_contract.team_options.append(year_string)
    if information["class"][1] == "salary-pl":
        player_contract.player_options.append(year_string)
    if information["class"][1] == "salary-et":
        player_contract.player_options.append(year_string)

class AllOfBasketball:

    players = []

    def __init__(self, years):

        ids = []

        all_basic_player_json = json.loads(requests.get('http://stats.nba.com/stats/commonallplayers', headers=headers, params=all_player_params).text)

        for resultSet in all_basic_player_json["resultSets"]:
            for player_json in resultSet["rowSet"]:
                if player_json[-1] == "Y":
                    if int(player_json[5]) >= int(years[0].split("-")[0]):
                        player = NBAObjects.Player(player_json[0], player_json[2], player_json[6])
                        ids.append(player_json[0])

        contract_soup = BeautifulSoup(requests.get("https://www.basketball-reference.com/contracts/players.html", headers=headers).text, "html.parser")

        for player_row in contract_soup.tbody.find_all('tr'):

            try:

                player_contract = NBAObjects.PlayerContract()
                years_and_info = player_row.find_all('td')

                player_contract.name = years_and_info[0].a.text
                player_contract.team = years_and_info[1].a.text

                player_contract.change_team("BRK", "BKN")
                player_contract.change_team("CHO", "CHA")
                player_contract.change_team("PHO", "PHX")

                contract_return(player_contract, player_contract.y1, years_and_info[2], "Year 1")
                contract_return(player_contract, player_contract.y2, years_and_info[3], "Year 2")
                contract_return(player_contract, player_contract.y3, years_and_info[4], "Year 3")
                contract_return(player_contract, player_contract.y4, years_and_info[5], "Year 4")
                contract_return(player_contract, player_contract.y5, years_and_info[6], "Year 5")
                contract_return(player_contract, player_contract.y6, years_and_info[7], "Year 6")

                player_contract.signed_using = years_and_info[8].text

                if NBAObjects.findByName(player.name):
                    NBAObjects.findByName(player.name).salary = player_contract

            except (IndexError, KeyError):
                continue

        for year in years:
            defParams = retStuff(year, "Defense")
            driveParams = retStuff(year, "Drives")
            efficiencyParams = retStuff(year, "Efficiency")
            passParams = retStuff(year, "Passing")
            postParams = retStuff(year, "PostTouch")

            session = FuturesSession()

            defResponse = session.get("http://stats.nba.com/stats/leaguedashptstats", headers=headers, params=defParams)
            defData = json.loads(defResponse.result().content)

            driveResponse = session.get("http://stats.nba.com/stats/leaguedashptstats", headers=headers, params=driveParams)
            driveData = json.loads(driveResponse.result().content)

            efficiencyResponse = session.get("http://stats.nba.com/stats/leaguedashptstats", headers=headers, params=efficiencyParams)
            efficiencyData = json.loads(efficiencyResponse.result().content)

            passResponse = session.get("http://stats.nba.com/stats/leaguedashptstats", headers=headers, params=passParams)
            passData = json.loads(passResponse.result().content)

            postResponse = session.get("http://stats.nba.com/stats/leaguedashptstats", headers=headers, params=postParams)
            postData = json.loads(postResponse.result().content)

            for player in defData["resultSets"][0]["rowSet"]:
                advanced = NBAObjects.PlayerTracking(year, player[11], player[12], player[13], "", "", "",
                "", "", "", "", "", "",
                "", "", "", "", "", "",
                "", "", "", "", "")
                NBAObjects.findById(player[0]).advanced_statistics.append(advanced)

            for player in driveData["resultSets"][0]["rowSet"]:
                advanced = NBAObjects.findById(player[0]).find_advanced_for_year(year)
                advanced.drivepts = player[15]
                advanced.driveast = player[19]
                advanced.drivepass = player[17]
                advanced.drivepf = player[23]
                advanced.drivefta = player[13]

            for player in efficiencyData["resultSets"][0]["rowSet"]:
                advanced = NBAObjects.findById(player[0]).find_advanced_for_year(year)
                advanced.pullupoints = player[13]
                advanced.catchshootpoints = player[11]
                advanced.posttouchpoints = player[17]
                advanced.elbowtouchpoints = player[19]

            for player in passData["resultSets"][0]["rowSet"]:
                advanced = NBAObjects.findById(player[0]).find_advanced_for_year(year)
                advanced.passesmade = player[8]
                advanced.passesreceived = player[9]
                advanced.secondaryassist = player[12]
                advanced.potentialassist = player[13]
                advanced.pointscreatedbyassist = player[14]
                advanced.overallassist = player[10]
            for player in postData["resultSets"][0]["rowSet"]:
                advanced = NBAObjects.findById(player[0]).find_advanced_for_year(year)
                advanced.postups = player[7]
                advanced.touches = player[8]
                advanced.postpasses = player[17]
                advanced.posttov = player[21]
                advanced.postpf = player[23]

            for player in NBAObjects.players:

                try:
                    params = (
                        ('LeagueID', '00'),
                        ('PerMode', 'PerGame'),
                        ('PlayerID', player.id)
                    )

                    id_param = (
                        ('PlayerID', player.id),
                        ('h', "h")
                    )

                    advanced_params = (
                        ('DateFrom', ''),
                        ('DateTo', ''),
                        ('GameSegment', ''),
                        ('LastNGames', '0'),
                        ('LeagueID', '00'),
                        ('Location', ''),
                        ('MeasureType', 'Advanced'),
                        ('Month', '0'),
                        ('OpponentTeamID', '0'),
                        ('Outcome', ''),
                        ('PORound', '0'),
                        ('PaceAdjust', 'N'),
                        ('PerMode', 'PerGame'),
                        ('PlayerID', player.id),
                        ('PlusMinus', 'N'),
                        ('Period', '0'),
                        ('Rank', 'N'),
                        ('Season', '2017-18'),
                        ('SeasonSegment', ''),
                        ('SeasonType', 'Regular Season'),
                        ('ShotClockRange', ''),
                        ('Split', 'yoy'),
                        ('VsConference', ''),
                        ('VsDivision', '')
                    )

                    session = FuturesSession()
                    height_weight_pos_response = session.get("http://stats.nba.com/stats/commonplayerinfo", headers=headers, params=id_param)
                    response = session.get("http://stats.nba.com/stats/playerprofilev2", headers=headers, params=params)
                    advanced_response = session.get("http://stats.nba.com/stats/playerdashboardbyyearoveryear", headers=headers, params=advanced_params)
                    common_html = height_weight_pos_response.result().content
                    common_data = json.loads(common_html)
                    player.height = common_data["resultSets"][0]["rowSet"][0][10]
                    player.weight = common_data["resultSets"][0]["rowSet"][0][11]
                    player.position = common_data["resultSets"][0]["rowSet"][0][14]

                    html = response.result().content
                    data = json.loads(html)
                    i = data["resultSets"][0]

                    for c in i["rowSet"]:
                        season = NBAObjects.OffensiveSeason(player.id, c[1], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10],
                        c[11], c[12], c[13], c[14], c[15], c[16], c[17], c[18], c[19],
                        c[20], c[21], c[22], c[23], c[24], c[25], c[26])
                        player.offensive_seasons.append(season)

                    html_advanced = advanced_response.result().content
                    data_advanced = json.loads(html_advanced)
                    i_advanced = data_advanced["resultSets"][1]

                    for c in i_advanced["rowSet"]:
                        season = NBAObjects.DefensiveSeason(player.id, c[2], c[3],
                        0, c[5], 0, c[9], c[6], c[7], c[8], c[10], c[11], c[12], c[13], c[14],
                        c[15], c[16], c[17], c[19], c[21], c[22], c[23], c[24], c[1])
                        player.defensive_seasons.append(season)

                    print("Gathering Data..." + player.name)
                    self.players.append(player)
                    time.sleep(0.2)

                except(KeyError, IndexError, ConnectionError):
                    print("Whoops, weird guy just appeared "+ player.name)

    def get_players(self):
        return self.players()
