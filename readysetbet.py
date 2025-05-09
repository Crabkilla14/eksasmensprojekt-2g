import tkinter as tk
from tkinter import messagebox
from balldontlie import BalldontlieAPI
from balldontlie.exceptions import (
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError,
    BallDontLieException
)

# Initialisér API
api_key = "00285fec-f3f2-4cb9-b7cd-6edc6b4102b7"
api = BalldontlieAPI(api_key)

# Fejlhåndtering
def handle_api_error(e):
    if isinstance(e, AuthenticationError):
        messagebox.showerror("Fejl", f"Ugyldig API-nøgle. ({e.status_code})")
    elif isinstance(e, RateLimitError):
        messagebox.showerror("Fejl", f"API-grænse overskredet. ({e.status_code})")
    elif isinstance(e, ValidationError):
        messagebox.showerror("Fejl", f"Ugyldige forespørgselsparametre. ({e.status_code})")
    elif isinstance(e, NotFoundError):
        messagebox.showerror("Fejl", f"Ressource ikke fundet. ({e.status_code})")
    elif isinstance(e, ServerError):
        messagebox.showerror("Fejl", f"Serverfejl. ({e.status_code})")
    elif isinstance(e, BallDontLieException):
        messagebox.showerror("Fejl", f"API-fejl. ({e.status_code})")
    else:
        messagebox.showerror("Ukendt fejl", str(e))

# Søg efter spiller og vis i GUI
def search_player():
    name = player_entry.get().strip()
    if not name:
        messagebox.showwarning("Inputfejl", "Indtast et spillernavn.")
        return

    try:
        players_response = api.nba.players.list(search=name)
        players = players_response.data

        if not players:
            messagebox.showinfo("Ingen resultater", f"Ingen spillere fundet med navnet '{name}'.")
            return

        player = players[0]
        player_id = player.id

        # Hent statistik korrekt via player_ids
        stats_response = api.nba.season_averages.get(player_ids=[player_id])
        stats = stats_response.data
        stat = stats[0] if stats else {}

        # Vis spillerinfo
        info = f"""
Navn: {player.first_name} {player.last_name}
Hold: {player.team.full_name if player.team else 'Ukendt'}
Position: {player.position or 'Ukendt'}
Højde: {player.height_feet or '?'}'{player.height_inches or '?'}
Vægt: {player.weight_pounds or '?'} lbs

Statistik (Seneste sæson):
Point (PTS): {stat.get('pts', 'N/A')}
Rebounds (REB): {stat.get('reb', 'N/A')}
Assists (AST): {stat.get('ast', 'N/A')}
Steals (STL): {stat.get('stl', 'N/A')}
Blocks (BLK): {stat.get('blk', 'N/A')}
"""
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, info.strip())
    except Exception as e:
        handle_api_error(e)

# Vis alle hold
def show_teams():
    try:
        teams_response = api.nba.teams.list()
        teams = teams_response.data

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, "NBA Hold:\n\n")
        for team in teams:
            text_output.insert(tk.END, f"{team.id}: {team.full_name} ({team.city})\n")
    except Exception as e:
        handle_api_error(e)

# ---------- GUI ----------
window = tk.Tk()
window.title("🏀 NBA Info Tool - GUI (med SDK)")
window.geometry("600x500")

frame = tk.Frame(window)
frame.pack(pady=10)

player_entry = tk.Entry(frame, width=30)
player_entry.grid(row=0, column=0, padx=5)

search_btn = tk.Button(frame, text="Søg spiller", command=search_player)
search_btn.grid(row=0, column=1, padx=5)

teams_btn = tk.Button(frame, text="Vis hold", command=show_teams)
teams_btn.grid(row=0, column=2, padx=5)

text_output = tk.Text(window, wrap=tk.WORD, width=70, height=25)
text_output.pack(pady=10)

window.mainloop()
