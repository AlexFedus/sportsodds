import requests
import json



API_KEY = "2d319702d293bc1f4ef00f963615da65"
SPORT = 'americanfootball_ncaaf' #'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'american' # decimal | american
DATE_FORMAT = 'iso' # iso | unix






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

    data = json.loads(odds_response.text)
    print()

    if SPORT=='americanfootball_nfl':

        sportsbookchoice = input("Choose your sportsbook: 'Barstool, DraftKings, or FanDual':  ")
        if (sportsbookchoice == "Barstool") or (sportsbookchoice == "barstool"):
            sportsbookNum = 3
        
        elif (sportchoice == "Draftkings" or (sportsbookchoice == "Draftkings") or (sportsbookchoice == "draftkings")):
            sportsbookNum = 16

        elif (sportchoice == "FanDual" or (sportsbookchoice == "fandual") or (sportsbookchoice == "Fandual")):
            sportsbookNum = 1

        else:
            sportsbookNum = -99
            print("Sorry, please enter one of the three sportsbook listed. (Barstool, DraftKings, Fandual")
            
        
        if sportsbookNum != -99:
            totaldata = len(data)
            i = 0
            while i < totaldata:
                home = (data[i]["home_team"])
                away = (data[i]["away_team"])
                sportsbook= (data[i]['bookmakers'][sportsbookNum]['title'])
                hometeam = (data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][1]['name'])
                awayteam = (data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][0]['name'])

                price=(data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][0]['price'])
                if int(price) > 0:
                    price = "+"+str(price)

                price2=(data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][1]['price'])
                if int(price2) > 0:
                    price2 = "+"+str(price2)

                points=(data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][0]['point'])
                if int(points) > 0:
                    points = "+"+str(points)
                
                points2=(data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][1]['point'])
                if int(points2) > 0:
                    points2 = "+"+str(points2)

                odds = (data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][0]['price'])
                if int(odds) > 0:
                    odds = "+"+str(odds)

                odds2 = (data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][1]['price'])
                if int(odds2) > 0:
                    odds2 = "+"+str(odds2)


                print(home, "at", away)
                print("   Sportsbook: " + sportsbook)
                print("   Moneyline:")
                print("      ",awayteam)
                print('         ',price)   
                print("      ",hometeam)
                print('         ',price2) 
                print("   Spread:")
                print("      ", awayteam)
                print("         Points: ", points)
                print("         Odds: ", odds)
                print("      ",hometeam)
                print("         Points: ", points2)
                print("         Odds: ", odds2)   
                print()

                i +=1
                
    elif SPORT=='americanfootball_ncaaf':
        
        sportsbookchoice = input("Choose your sportsbook: 'Barstool or DraftKings':  ")
        if (sportsbookchoice == "Barstool") or (sportsbookchoice == "barstool"):
            sportsbookNum = 7
        
        elif (sportchoice == "Draftkings" or (sportsbookchoice == "Draftkings") or (sportsbookchoice == "draftkings")):
            sportsbookNum = 1

        else:
            sportsbookNum = -99
            print("Sorry, please enter one of the three sportsbook listed. (Barstool, DraftKings, Fandual")
            
        
        if sportsbookNum != -99:
            totaldata = len(data)
            i = 0
            while i < totaldata:
                home = (data[i]["home_team"])
                away = (data[i]["away_team"])
                sportsbook= (data[i]['bookmakers'][sportsbookNum]['title'])
                hometeam = (data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][1]['name'])
                awayteam = (data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][0]['name'])

                price=(data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][0]['price'])
                if int(price) > 0:
                    price = "+"+str(price)

                price2=(data[i]['bookmakers'][sportsbookNum]['markets'][0]['outcomes'][1]['price'])
                if int(price2) > 0:
                    price2 = "+"+str(price2)

                points=(data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][0]['point'])
                if int(points) > 0:
                    points = "+"+str(points)
                
                points2=(data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][1]['point'])
                if int(points2) > 0:
                    points2 = "+"+str(points2)

                odds = (data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][0]['price'])
                if int(odds) > 0:
                    odds = "+"+str(odds)

                odds2 = (data[i]['bookmakers'][sportsbookNum]['markets'][1]['outcomes'][1]['price'])
                if int(odds2) > 0:
                    odds2 = "+"+str(odds2)


                print(home, "at", away)
                print("   Sportsbook: " + sportsbook)
                print("   Moneyline:")
                print("      ",awayteam)
                print('         ',price)   
                print("      ",hometeam)
                print('         ',price2) 
                print("   Spread:")
                print("      ", awayteam)
                print("         Points: ", points)
                print("         Odds: ", odds)
                print("      ",hometeam)
                print("         Points: ", points2)
                print("         Odds: ", odds2)   
                print()

                i +=1
        
        


""""
    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print()
    print('Used requests', odds_response.headers['x-requests-used'])
"""
