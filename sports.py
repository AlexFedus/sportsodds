import tkinter as tk
from tkinter import ttk
import requests
import json
from DateConverter import *
import zoneinfo



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #API_KEY = "2d319702d293bc1f4ef00f963615da65"
        API_KEY = "74991ddf5f36ad6f09f21d4c7143aecd"   
        REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
        MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
        ODDS_FORMAT = 'american' # decimal | american
        DATE_FORMAT = 'iso' # iso | unix
        
        # Set the size of the window and center it on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 600
        x_coord = (screen_width // 2) - (window_width // 2)
        y_coord = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{x_coord}+{y_coord}')
        
        # Use the 'clam' theme
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Create the frames for each sport
        self.ncaa_frame = tk.Frame(self)
        self.nfl_frame = tk.Frame(self)
        
        # Create the widgets for the NCAA frame
        ncaa_label = ttk.Label(self.ncaa_frame, text='NCAA Football')
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

        
        ncaa_listbox = tk.Listbox(self.ncaa_frame, width=75)
        ncaa_listbox.pack(fill='both', expand=True)

        total_ncaa_data = len(ncaa_data)
        i = 0
        while i < total_ncaa_data:
            print(i)

            hometeam = ncaa_data[i]["home_team"]
            awayteam = ncaa_data[i]["away_team"]


            matchupstring = awayteam + " VS " + hometeam
            ncaa_listbox.insert('end', matchupstring)
            ncaa_listbox.itemconfig('end', {'bg':'red'})


            dateTime = ncaa_data[i]["commence_time"]
            ncaa_listbox.insert('end', str(convertDate(dateTime)) + " EST")
            ncaa_listbox.itemconfig('end', {'bg':'red'})

            bookmakertotal = len(ncaa_data[i])
            b = 0
            while b < bookmakertotal:
                sportsbook = ncaa_data[i]["bookmakers"][b]["title"]

                try:
                    spreadname = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["name"]
                    spreadprice = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["point"]
                    spreadodd = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][0]["price"]

                    spreadname2 = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["name"]
                    spreadprice2 = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["point"]
                    spreadodd2 = ncaa_data[i]["bookmakers"][b]["markets"][1]["outcomes"][1]["price"]

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


                
                
                

                moneyname = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["name"]
                moneyodd = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][0]["price"]
                moneyname2 = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["name"]
                moneyodd2 = ncaa_data[i]["bookmakers"][b]["markets"][0]["outcomes"][1]["price"]


                if(moneyodd > 0):
                    moneyodd = str("+"+str(moneyodd))
                if(moneyodd2 > 0):
                    moneyodd2 = str("+"+str(moneyodd2))

                moneylinestring = moneyname + " " + str(moneyodd)
                moneylinestring2 = moneyname2 + " " + str(moneyodd2)
                ncaa_listbox.insert('end', "        "+sportsbook)
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
        
 
        # Create the widgets for the NFL frame
        nfl_label = ttk.Label(self.nfl_frame, text='NFL Football')
        nfl_label.pack(pady=10)
        back_button = ttk.Button(self.nfl_frame, text='Back', command=self.show_default)
        back_button.pack(side='right')

        # Get the NFL data and display it

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
            print(i)

            hometeam = nfl_data[i]["home_team"]
            awayteam = nfl_data[i]["away_team"]
            matchupstring = awayteam + " VS " + hometeam
            nfl_listbox.insert('end', matchupstring)
            nfl_listbox.itemconfig('end', {'bg':'red'})


            dateTime = nfl_data[i]["commence_time"]
            nfl_listbox.insert('end', str(convertDate(dateTime)) + " EST")
            nfl_listbox.itemconfig('end', {'bg':'red'})

            bookmakertotal = len(nfl_data[i])
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

    

        # Create the default frame and its widgets
        self.default_frame = tk.Frame(self)
        default_label = ttk.Label(self.default_frame, text='Choose a sport:')
        default_label.pack(pady=10)
        ncaa_button = ttk.Button(self.default_frame, text='NCAA Football', command=self.show_ncaa)
        nfl_button = ttk.Button(self.default_frame, text='NFL Football', command=self.show_nfl)
        ncaa_button.pack(side='left')
        nfl_button.pack(side='left')

        # Show the default frame by default
        self.show_default()

    def show_ncaa(self):
        self.ncaa_frame.pack(fill='both', expand=True)
        self.nfl_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_nfl(self):
        self.nfl_frame.pack(fill="both", expand=True)
        self.ncaa_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_default(self):
        self.default_frame.pack()
        self.ncaa_frame.pack_forget()
        self.nfl_frame.pack_forget()

app = App()
app.mainloop()

