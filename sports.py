import tkinter as tk
from tkinter import ttk
import requests
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        API_KEY = "2d319702d293bc1f4ef00f963615da65"
        REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
        MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
        ODDS_FORMAT = 'american' # decimal | american
        DATE_FORMAT = 'iso' # iso | unix
        
        # Set the size of the window and center it on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 600
        window_height = 400
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
        ncaa_text = tk.Text(self.ncaa_frame)
        ncaa_text.pack(fill='both', expand=True)
        ncaa_text.insert('1.0', json.dumps(ncaa_data, indent=4))

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
        nfl_text = tk.Text(self.nfl_frame)
        nfl_text.pack(fill='both', expand=True)
        nfl_text.insert('1.0', json.dumps(nfl_data, indent=4))

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
        self.ncaa_frame.pack()
        self.nfl_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_nfl(self):
        self.nfl_frame.pack()
        self.ncaa_frame.pack_forget()
        self.default_frame.pack_forget()

    def show_default(self):
        self.default_frame.pack()
        self.ncaa_frame.pack_forget()
        self.nfl_frame.pack_forget()

app = App()
app.mainloop()

