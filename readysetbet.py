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

if __name__ == "__main__":
    main_menu()
