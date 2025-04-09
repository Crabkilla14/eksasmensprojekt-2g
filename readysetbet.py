import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from PIL import Image
from io import BytesIO
import webbrowser
import os

console = Console()
API_URL = "https://www.balldontlie.io/api/v1"

def main_menu():
    while True:
        console.print(Panel("🏀 [bold yellow]Ready, Set, Bet! - NBA Info Tool[/bold yellow]", expand=False))
        console.print("1. Søg efter spiller")
        console.print("2. Vis hold")
        console.print("3. Afslut")
        choice = input("\nVælg et nummer: ")

        if choice == "1":
            search_player()
        elif choice == "2":
            show_teams()
        elif choice == "3":
            console.print("Farvel 👋")
            break
        else:
            console.print("[red]Ugyldigt valg. Prøv igen.[/red]")

def search_player():
    name = input("Indtast spillerens navn: ")
    response = requests.get(f"{API_URL}/players", params={"search": name})
    players = response.json()["data"]

    if not players:
        console.print("[red]Ingen spillere fundet.[/red]")
        return

    player = players[0]  # vælg første resultat
    player_id = player["id"]

    # Hent stats
    stats_response = requests.get(f"{API_URL}/season_averages", params={"player_ids[]": player_id})
    stats = stats_response.json()["data"]
    stats_data = stats[0] if stats else {}

    # Lav visning
    table = Table(title=f"{player['first_name']} {player['last_name']} - Info")

    table.add_column("Felt", style="cyan", no_wrap=True)
    table.add_column("Værdi", style="magenta")

    table.add_row("Hold", player['team']['full_name'])
    table.add_row("Position", player['position'] or "Ukendt")
    table.add_row("Højde", f"{player['height_feet'] or '?'}'{player['height_inches'] or '?'}")
    table.add_row("Vægt", f"{player['weight_pounds'] or '?'} lbs")

    for key in ['pts', 'reb', 'ast', 'stl', 'blk']:
        table.add_row(key.upper(), str(stats_data.get(key, "N/A")))

    console.print(table)

    # Prøv at åbne billede (brug nba.com som billedeksempel)
    fake_img_url = f"https://nba-players.herokuapp.com/players/{player['last_name'].lower()}/{player['first_name'].lower()}"
    try:
        webbrowser.open(fake_img_url)
        console.print(f"[green]Åbner billede i browser: {fake_img_url}[/green]")
    except:
        console.print("[yellow]Kunne ikke åbne billede.[/yellow]")

def show_teams():
    response = requests.get(f"{API_URL}/teams")
    teams = response.json()["data"]

    table = Table(title="NBA Hold")

    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Holdnavn", style="magenta")
    table.add_column("By", style="green")

    for team in teams:
        table.add_row(str(team["id"]), team["full_name"], team["city"])

    console.print(table)

if __name__ == "__main__":
    main_menu()
