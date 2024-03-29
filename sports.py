import tkinter as tk
from tkinter import ttk
import requests
import json
from DateConverter import *
import zoneinfo
from tkinter import messagebox
import config



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        
        API_KEY = config.API_KEY
          
        # Configures API parameters
        REGIONS = 'us'
        MARKETS = 'h2h,spreads' 
        ODDS_FORMAT = 'american' 
        DATE_FORMAT = 'iso' 
        
        # Centers window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 600
        x_coord = (screen_width // 2) - (window_width // 2)
        y_coord = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{x_coord}+{y_coord}')
        
        
        # Applies the Clam theme
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Creates the frames for each sport
        self.ncaa_frame = tk.Frame(self)
        self.nfl_frame = tk.Frame(self)
        self.nba_frame = tk.Frame(self)
        self.nhl_frame = tk.Frame(self)

        # Creates the widgets for the NCAA frame
        ncaa_label = ttk.Label(self.ncaa_frame, text='NCAA Football')
        ncaa_label.config(font="Times 32")
        ncaa_label.pack(pady=10)
        back_button = ttk.Button(self.ncaa_frame, text='Back', command=self.show_default)
        back_button.pack(side='right')

        
        # Get the NCAA data and display it
        ncaa_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/americanfootball_ncaaf/odds',
            params={
                'api_key': API_KEY,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }
        )

        ncaa_data = json.loads(ncaa_response.text)

        # Creates a listbox to display the data
        ncaa_listbox = tk.Listbox(self.ncaa_frame, width=75)
        ncaa_listbox.pack(fill='both', expand=True)
        
        
        # Gathers and displays all matchups
        total_ncaa_data = len(ncaa_data)
        i = 0
        while i < total_ncaa_data:

            # Sets the home and away teams to variables
            hometeam = ncaa_data[i]["home_team"]
            awayteam = ncaa_data[i]["away_team"]


            matchupstring = awayteam + " VS " + hometeam
            ncaa_listbox.insert('end', matchupstring)
            ncaa_listbox.itemconfig('end', {'bg':'red'})

            #Gets the time of the event and converts it to a readable format
            dateTime = ncaa_data[i]["commence_time"]
            ncaa_listbox.insert('end', str(convertDate(dateTime)) + " EST")
            ncaa_listbox.itemconfig('end', {'bg':'red'})

            # Gathers and displays all Sportsbooks with moneyline odds along with spread odds
            bookmakertotal = len(ncaa_data[i]["bookmakers"])
            b = 0
            while b < bookmakertotal:
                sportsbook = ncaa_data[i]["bookmakers"][b]["title"]

                # Tries to get data for spreads and setting variables as null if they are not in the api
                try:
                    spreadname = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["name"]
                    spreadprice = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["point"]
                    spreadodd = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["price"]

                    spreadname2 = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["name"]
                    spreadprice2 = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["point"]
                    spreadodd2 = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["price"]

                    # Adds a plus sign in front of positive numbers
                    if(spreadprice > 0):
                        spreadprice = str("+"+str(spreadprice))
                    if(spreadodd > 0):
                        spreadodd = str("+"+str(spreadodd))
                    if(spreadprice2 > 0):
                        spreadprice2 = str("+"+str(spreadprice2))
                    if(spreadodd2 > 0):
                        spreadodd2 = str("+"+str(spreadodd2))
                
                except:
                    spreadname = "null"
                    spreadprice = "null"
                    spreadodd = "null"

                    spreadname2 = "null"
                    spreadprice2 = "null"
                    spreadodd2 = "null"


                
                
                
                # Gets moneyline odds
                moneyname = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["name"]
                moneyodd = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["price"]
                moneyname2 = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["name"]
                moneyodd2 = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["price"]

                # Adds a plus sign if odds are greater then 0
                if(moneyodd > 0):
                    moneyodd = str("+"+str(moneyodd))
                if(moneyodd2 > 0):
                    moneyodd2 = str("+"+str(moneyodd2))

                moneylinestring = moneyname + " " + str(moneyodd)
                moneylinestring2 = moneyname2 + " " + str(moneyodd2)
                ncaa_listbox.insert('end', "        "+sportsbook)
                
                
                #Adds data to the listbox
                ncaa_listbox.itemconfig('end', {'bg':'lightgreen'})

                ncaa_listbox.insert('end', "                Spread -     " + str(spreadname))
                ncaa_listbox.itemconfig('end', {'bg':'lightblue'})

                ncaa_listbox.insert('end', "                                        Point    " + str(spreadprice))
                ncaa_listbox.itemconfig('end', {'bg':'lightblue'})

                ncaa_listbox.insert('end', "                                        Odds     " + str(spreadodd))
                ncaa_listbox.itemconfig('end', {'bg':'lightblue'})

                ncaa_listbox.insert('end', "                             " + str(spreadname2))
                ncaa_listbox.itemconfig('end', {'bg':'lightblue'})

                ncaa_listbox.insert('end', "                                        Point    " + str(spreadprice2))
                ncaa_listbox.itemconfig('end', {'bg':'lightblue'})

                ncaa_listbox.insert('end', "                                        Odds     " + str(spreadodd2))
                ncaa_listbox.itemconfig('end', {'bg':'lightblue'})

                ncaa_listbox.insert('end', "                Moneyline -  " + moneylinestring)
                ncaa_listbox.itemconfig('end', {'bg':'orange'})

                ncaa_listbox.insert('end', "                                      " + moneylinestring2)
                ncaa_listbox.itemconfig('end', {'bg':'orange'})

                b += 1

            i += 1
            ncaa_listbox.insert('end', "")
            ncaa_listbox.config(font="Times 16")
        
 
        # Creates the widgets for the NFL frame
        nfl_label = ttk.Label(self.nfl_frame, text='NFL Football')
        nfl_label.config(font="Times 32")
        nfl_label.pack(pady=10)
        back_button = ttk.Button(self.nfl_frame, text='Back', command=self.show_default)
        back_button.pack(side='right')

        # Gets the NFL data and display it

        nfl_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds',
            params={
                'api_key': API_KEY,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }
        )
        
        

        nfl_data = json.loads(nfl_response.text)

        
        nfl_listbox = tk.Listbox(self.nfl_frame, width=75)
        nfl_listbox.pack(fill='both', expand=True)

        total_nfl_data = len(nfl_data)
        i = 0
        while i < total_nfl_data:

            hometeam = nfl_data[i]["home_team"]
            awayteam = nfl_data[i]["away_team"]
            matchupstring = awayteam + " VS " + hometeam
            nfl_listbox.insert('end', matchupstring)
            nfl_listbox.itemconfig('end', {'bg':'red'})


            dateTime = nfl_data[i]["commence_time"]
            nfl_listbox.insert('end', str(convertDate(dateTime)) + " EST")
            nfl_listbox.itemconfig('end', {'bg':'red'})

            bookmakertotal = len(nfl_data[i]["bookmakers"])
            b = 0
            while b < bookmakertotal:
                sportsbook = nfl_data[i]["bookmakers"][b]["title"]

                try:
                    spreadname = nfl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["name"]
                    spreadprice = nfl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["point"]
                    spreadodd = nfl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["price"]

                    spreadname2 = nfl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["name"]
                    spreadprice2 = nfl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["point"]
                    spreadodd2 = nfl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["price"]

                    if(spreadprice > 0):
                        spreadprice = str("+"+str(spreadprice))
                    if(spreadodd > 0):
                        spreadodd = str("+"+str(spreadodd))
                    if(spreadprice2 > 0):
                        spreadprice2 = str("+"+str(spreadprice2))
                    if(spreadodd2 > 0):
                        spreadodd2 = str("+"+str(spreadodd2))
                
                except:
                    spreadname = "null"
                    spreadprice = "null"
                    spreadodd = "null"

                    spreadname2 = "null"
                    spreadprice2 = "null"
                    spreadodd2 = "null"


                
                
                

                moneyname = nfl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["name"]
                moneyodd = nfl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["price"]
                moneyname2 = nfl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["name"]
                moneyodd2 = nfl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["price"]


                if(moneyodd > 0):
                    moneyodd = str("+"+str(moneyodd))
                if(moneyodd2 > 0):
                    moneyodd2 = str("+"+str(moneyodd2))

                moneylinestring = moneyname + " " + str(moneyodd)
                moneylinestring2 = moneyname2 + " " + str(moneyodd2)
                nfl_listbox.insert('end', "        "+sportsbook)
                nfl_listbox.itemconfig('end', {'bg':'lightgreen'})

                nfl_listbox.insert('end', "                Spread -     " + str(spreadname))
                nfl_listbox.itemconfig('end', {'bg':'lightblue'})

                nfl_listbox.insert('end', "                                        Point    " + str(spreadprice))
                nfl_listbox.itemconfig('end', {'bg':'lightblue'})

                nfl_listbox.insert('end', "                                        Odds     " + str(spreadodd))
                nfl_listbox.itemconfig('end', {'bg':'lightblue'})

                nfl_listbox.insert('end', "                             " + str(spreadname2))
                nfl_listbox.itemconfig('end', {'bg':'lightblue'})

                nfl_listbox.insert('end', "                                        Point    " + str(spreadprice2))
                nfl_listbox.itemconfig('end', {'bg':'lightblue'})

                nfl_listbox.insert('end', "                                        Odds     " + str(spreadodd2))
                nfl_listbox.itemconfig('end', {'bg':'lightblue'})

                nfl_listbox.insert('end', "                Moneyline -  " + moneylinestring)
                nfl_listbox.itemconfig('end', {'bg':'orange'})

                nfl_listbox.insert('end', "                                      " + moneylinestring2)
                nfl_listbox.itemconfig('end', {'bg':'orange'})

                b += 1

            i += 1
            nfl_listbox.insert('end', "")
            nfl_listbox.config(font="Times 16")

    
        # Create the widgets for the NBA frame
        nba_label = ttk.Label(self.nba_frame, text='NBA Basketball')
        nba_label.config(font="Times 32")
        nba_label.pack(pady=10)
        back_button = ttk.Button(self.nba_frame, text='Back', command=self.show_default)
        back_button.pack(side='right')

        # Get the NFL data and display it

        nba_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/basketball_nba/odds',
            params={
                'api_key': API_KEY,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }
        )
        
        

        nba_data = json.loads(nba_response.text)

        
        nba_listbox = tk.Listbox(self.nba_frame, width=75)
        nba_listbox.pack(fill='both', expand=True)

        total_nba_data = len(nba_data)
        i = 0
        while i < total_nba_data:

            hometeam = nba_data[i]["home_team"]
            awayteam = nba_data[i]["away_team"]
            matchupstring = awayteam + " VS " + hometeam
            nba_listbox.insert('end', matchupstring)
            nba_listbox.itemconfig('end', {'bg':'red'})


            dateTime = nba_data[i]["commence_time"]
            nba_listbox.insert('end', str(convertDate(dateTime)) + " EST")
            nba_listbox.itemconfig('end', {'bg':'red'})

            bookmakertotal = len(nba_data[i]["bookmakers"])
            b = 0
            while b < bookmakertotal:

                sportsbook = nba_data[i]["bookmakers"][b]["title"]

                try:
                    spreadname = nba_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["name"]
                    spreadprice = nba_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["point"]
                    spreadodd = nba_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["price"]

                    spreadname2 = nba_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["name"]
                    spreadprice2 = nba_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["point"]
                    spreadodd2 = nba_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["price"]

                    if(spreadprice > 0):
                        spreadprice = str("+"+str(spreadprice))
                    if(spreadodd > 0):
                        spreadodd = str("+"+str(spreadodd))
                    if(spreadprice2 > 0):
                        spreadprice2 = str("+"+str(spreadprice2))
                    if(spreadodd2 > 0):
                        spreadodd2 = str("+"+str(spreadodd2))
                
                except:
                    spreadname = "null"
                    spreadprice = "null"
                    spreadodd = "null"

                    spreadname2 = "null"
                    spreadprice2 = "null"
                    spreadodd2 = "null"


                
                
                

                moneyname = nba_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["name"]
                moneyodd = nba_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["price"]
                moneyname2 = nba_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["name"]
                moneyodd2 = nba_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["price"]


                if(moneyodd > 0):
                    moneyodd = str("+"+str(moneyodd))
                if(moneyodd2 > 0):
                    moneyodd2 = str("+"+str(moneyodd2))

                moneylinestring = moneyname + " " + str(moneyodd)
                moneylinestring2 = moneyname2 + " " + str(moneyodd2)
                nba_listbox.insert('end', "        "+sportsbook)
                nba_listbox.itemconfig('end', {'bg':'lightgreen'})

                nba_listbox.insert('end', "                Spread -     " + str(spreadname))
                nba_listbox.itemconfig('end', {'bg':'lightblue'})

                nba_listbox.insert('end', "                                        Point    " + str(spreadprice))
                nba_listbox.itemconfig('end', {'bg':'lightblue'})

                nba_listbox.insert('end', "                                        Odds     " + str(spreadodd))
                nba_listbox.itemconfig('end', {'bg':'lightblue'})

                nba_listbox.insert('end', "                             " + str(spreadname2))
                nba_listbox.itemconfig('end', {'bg':'lightblue'})

                nba_listbox.insert('end', "                                        Point    " + str(spreadprice2))
                nba_listbox.itemconfig('end', {'bg':'lightblue'})

                nba_listbox.insert('end', "                                        Odds     " + str(spreadodd2))
                nba_listbox.itemconfig('end', {'bg':'lightblue'})

                nba_listbox.insert('end', "                Moneyline -  " + moneylinestring)
                nba_listbox.itemconfig('end', {'bg':'orange'})

                nba_listbox.insert('end', "                                      " + moneylinestring2)
                nba_listbox.itemconfig('end', {'bg':'orange'})

                b += 1

            i += 1
            nba_listbox.insert('end', "")
            nba_listbox.config(font="Times 16")

    


        # Create the widgets for the NHL frame
        nhl_label = ttk.Label(self.nhl_frame, text='NHL Hockey')
        nhl_label.config(font="Times 32")
        nhl_label.pack(pady=10)
        back_button = ttk.Button(self.nhl_frame, text='Back', command=self.show_default)
        back_button.pack(side='right')

        # Get the NFL data and display it

        nhl_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds',
            params={
                'api_key': API_KEY,
                'regions': REGIONS,
                'markets': MARKETS,
                'oddsFormat': ODDS_FORMAT,
                'dateFormat': DATE_FORMAT,
            }
        )
        
        

        nhl_data = json.loads(nhl_response.text)

        
        nhl_listbox = tk.Listbox(self.nhl_frame, width=75)
        nhl_listbox.pack(fill='both', expand=True)

        total_nhl_data = len(nhl_data)
        i = 0
        while i < total_nhl_data:

            hometeam = nhl_data[i]["home_team"]
            awayteam = nhl_data[i]["away_team"]
            matchupstring = awayteam + " VS " + hometeam
            nhl_listbox.insert('end', matchupstring)
            nhl_listbox.itemconfig('end', {'bg':'red'})


            dateTime = nhl_data[i]["commence_time"]
            nhl_listbox.insert('end', str(convertDate(dateTime)) + " EST")
            nhl_listbox.itemconfig('end', {'bg':'red'})

            bookmakertotal = len(nhl_data[i]["bookmakers"])
            b = 0
            while b < bookmakertotal:

                sportsbook = nhl_data[i]["bookmakers"][b]["title"]

                try:
                    spreadname = nhl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["name"]
                    spreadprice = nhl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["point"]
                    spreadodd = nhl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["price"]

                    spreadname2 = nhl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["name"]
                    spreadprice2 = nhl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["point"]
                    spreadodd2 = nhl_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["price"]

                    if(spreadprice > 0):
                        spreadprice = str("+"+str(spreadprice))
                    if(spreadodd > 0):
                        spreadodd = str("+"+str(spreadodd))
                    if(spreadprice2 > 0):
                        spreadprice2 = str("+"+str(spreadprice2))
                    if(spreadodd2 > 0):
                        spreadodd2 = str("+"+str(spreadodd2))
                
                except:
                    spreadname = "null"
                    spreadprice = "null"
                    spreadodd = "null"

                    spreadname2 = "null"
                    spreadprice2 = "null"
                    spreadodd2 = "null"


                
                
                

                moneyname = nhl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["name"]
                moneyodd = nhl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["price"]
                moneyname2 = nhl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["name"]
                moneyodd2 = nhl_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["price"]


                if(moneyodd > 0):
                    moneyodd = str("+"+str(moneyodd))
                if(moneyodd2 > 0):
                    moneyodd2 = str("+"+str(moneyodd2))

                moneylinestring = moneyname + " " + str(moneyodd)
                moneylinestring2 = moneyname2 + " " + str(moneyodd2)
                nhl_listbox.insert('end', "        "+sportsbook)
                nhl_listbox.itemconfig('end', {'bg':'lightgreen'})

                nhl_listbox.insert('end', "                Spread -     " + str(spreadname))
                nhl_listbox.itemconfig('end', {'bg':'lightblue'})

                nhl_listbox.insert('end', "                                        Point    " + str(spreadprice))
                nhl_listbox.itemconfig('end', {'bg':'lightblue'})

                nhl_listbox.insert('end', "                                        Odds     " + str(spreadodd))
                nhl_listbox.itemconfig('end', {'bg':'lightblue'})

                nhl_listbox.insert('end', "                             " + str(spreadname2))
                nhl_listbox.itemconfig('end', {'bg':'lightblue'})

                nhl_listbox.insert('end', "                                        Point    " + str(spreadprice2))
                nhl_listbox.itemconfig('end', {'bg':'lightblue'})

                nhl_listbox.insert('end', "                                        Odds     " + str(spreadodd2))
                nhl_listbox.itemconfig('end', {'bg':'lightblue'})

                nhl_listbox.insert('end', "                Moneyline -  " + moneylinestring)
                nhl_listbox.itemconfig('end', {'bg':'orange'})

                nhl_listbox.insert('end', "                                      " + moneylinestring2)
                nhl_listbox.itemconfig('end', {'bg':'orange'})

                b += 1

            i += 1
            nhl_listbox.insert('end', "")
            nhl_listbox.config(font="Times 16")

    




        # Create the default frame and its widgets
        self.default_frame = tk.Frame(self)
        default_label = ttk.Label(self.default_frame, text='Choose a sport:', font=('Times 32'))
        default_label.pack(pady=10)
        ncaa_button = ttk.Button(self.default_frame, text='NCAA Football', command=self.show_ncaa)
        nfl_button = ttk.Button(self.default_frame, text='NFL Football', command=self.show_nfl)
        nba_button = ttk.Button(self.default_frame, text='NBA Basketball', command=self.show_nba)
        nhl_button = ttk.Button(self.default_frame, text='NHL Hockey', command=self.show_nhl)

        ncaa_button.pack(side='top', pady = 15)
        nfl_button.pack(side='top', pady = 15)
        nba_button.pack(side='top', pady = 15)
        nhl_button.pack(side='top', pady = 15)

        # Show the default frame by default
        self.show_default()

    def show_ncaa(self):
        self.ncaa_frame.pack(fill='both', expand=True)
        self.nfl_frame.pack_forget()
        self.nba_frame.pack_forget()
        self.nhl_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_nfl(self):
        self.nfl_frame.pack(fill="both", expand=True)
        self.ncaa_frame.pack_forget()
        self.nba_frame.pack_forget()
        self.nhl_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_nba(self):
        self.nba_frame.pack(fill="both", expand = True)
        self.ncaa_frame.pack_forget()
        self.nfl_frame.pack_forget()
        self.nhl_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_nhl(self):
        self.nhl_frame.pack(fill="both", expand = True)
        self.ncaa_frame.pack_forget()
        self.nfl_frame.pack_forget()
        self.nba_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_default(self):
        self.default_frame.pack()
        self.ncaa_frame.pack_forget()
        self.nfl_frame.pack_forget()
        self.nba_frame.pack_forget()
        self.nhl_frame.pack_forget()

app = App()
app.mainloop()

