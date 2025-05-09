<<<<<<< HEAD
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
=======
import requests
import webbrowser
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

API_URL = "https://www.balldontlie.io/api/v1"
console = Console()

def main_menu():
    while True:
        console.clear()
        console.print(Panel("[bold blue]🏀 Ready, Set, Bet! - NBA Info Explorer[/bold blue]"))
        console.print("[1] Søg efter spiller")
        console.print("[2] Vis alle NBA-hold")
        console.print("[3] Afslut\n")

        valg = input("Vælg en mulighed: ").strip()
        if valg == "1":
            søg_spiller()
        elif valg == "2":
            vis_hold()
        elif valg == "3":
            console.print("\n[green]Tak for spillet![/green] 👋")
            break
        else:
            console.print("[red]Ugyldigt valg. Prøv igen.[/red]\n")
            input("Tryk Enter for at fortsætte...")

def søg_spiller():
    console.clear()
    navn = input("Indtast spillerens navn (f.eks. LeBron): ").strip()

    try:
        response = requests.get(f"{API_URL}/players", params={"search": navn})

        if response.status_code != 200:
            console.print(f"[red]Fejl fra API: {response.status_code}[/red]")
            input("Tryk Enter for at vende tilbage...")
            return

        data = response.json().get("data", [])
        if not data:
            console.print("[red]Ingen spillere fundet med det navn.[/red]")
            input("Tryk Enter for at vende tilbage...")
            return

        spiller = data[0]
        id = spiller['id']
        stats_response = requests.get(f"{API_URL}/season_averages", params={"player_ids[]": id})
        stats = stats_response.json().get("data", [])

        table = Table(title=f"{spiller['first_name']} {spiller['last_name']} - Info")
        table.add_column("Felt", style="cyan")
        table.add_column("Værdi", style="magenta")

        table.add_row("Hold", spiller['team']['full_name'])
        table.add_row("Position", spiller['position'] or "Ukendt")
        table.add_row("Højde", f"{spiller['height_feet'] or '?'}'{spiller['height_inches'] or '?'}")
        table.add_row("Vægt", f"{spiller['weight_pounds'] or '?'} lbs")

        if stats:
            s = stats[0]
            table.add_row("PPG", str(s.get("pts", "N/A")))
            table.add_row("AST", str(s.get("ast", "N/A")))
            table.add_row("REB", str(s.get("reb", "N/A")))
            table.add_row("STL", str(s.get("stl", "N/A")))
            table.add_row("BLK", str(s.get("blk", "N/A")))
        else:
            table.add_row("Stats", "Ingen tilgængelige stats for denne sæson.")

        console.print(table)

        # Åbn billede
        navn_url = f"{spiller['last_name'].lower()}/{spiller['first_name'].lower()}"
        fake_img_url = f"https://nba-players.herokuapp.com/players/{navn_url}"
        webbrowser.open(fake_img_url)
        console.print(f"[blue]Åbner billede i browser: {fake_img_url}[/blue]")

    except Exception as e:
        console.print(f"[red]Noget gik galt: {e}[/red]")

    input("\nTryk Enter for at gå tilbage til menuen...")


def vis_hold():
    console.clear()
    response = requests.get(f"{API_URL}/teams")
    teams = response.json()["data"]

    table = Table(title="NBA Hold")
    table.add_column("ID", style="cyan")
    table.add_column("Holdnavn", style="green")
    table.add_column("By", style="magenta")

    for hold in teams:
        table.add_row(str(hold['id']), hold['full_name'], hold['city'])

    console.print(table)
    input("\nTryk Enter for at gå tilbage til menuen...")
>>>>>>> 9f63fda23cc4c6abeb345e5575ce773f6ed29f95

search_btn = tk.Button(frame, text="Søg spiller", command=search_player)
search_btn.grid(row=0, column=1, padx=5)

teams_btn = tk.Button(frame, text="Vis hold", command=show_teams)
teams_btn.grid(row=0, column=2, padx=5)

text_output = tk.Text(window, wrap=tk.WORD, width=70, height=25)
text_output.pack(pady=10)

window.mainloop()
