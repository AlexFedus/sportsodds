import requests
import json
import pprint


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = "2d319702d293bc1f4ef00f963615da65"

SPORT = 'americanfootball_ncaaf' #'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'american' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports?apiKey='+API_KEY
)

#(sports_response.json())


"""
if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    data = json.loads(sports_response.text)
   # pprint.pprint(data)

    totaldata = len(data)-1
    i = 0
    while i < totaldata:
        print(data[i]["title"])
        i +=1


   # group = data[0]["title"]
   # title = data[1]["title"]

  #  print(group, "  ", title)

"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sportchoice= (input("Choose NCAA or NFL:  "))

if (sportchoice == 'ncaa') or (sportchoice == "NCAA"):
    SPORT = 'americanfootball_ncaaf'

else:
    SPORT = 'americanfootball_nfl'    

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:

    """
    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    print()
    print(odds_json)
    print()
    """

    data = json.loads(odds_response.text)
   # pprint.pprint(data)

    print()

    totaldata = len(data)-1
    i = 1
    while i < totaldata:
        print(data[i]["home_team"])
        print(data[i]["away_team"])
        print()
        i +=1


""""
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print()
    print('Used requests', odds_response.headers['x-requests-used'])
"""
