# Ready, Set, Bet!
Gustas og Cornelius

## Kort projektbeskrivelse
Vores projekt er en Python-applikation, der bruger den offentlige NBA API (balldontlie.io) til at hente og vise spillerinformation og statistikker. Applikationen er rettet mod NBA-fans og gamblere, som hurtigt skal bruge data til at vælge spillere til deres parlay eller fantasy-hold.

## Kravspecifikation

| Krav                                                                 | 
|----------------------------------------------------------------------|
| Programmet viser billeder og info om spillere                        | 
| Programmet har en overskuelig menu                                   | 
| Programmet viser information i separat konsol med flot layout        |      
| Programmet henter stats via brugerinput (fx navn, hold, ppg osv.)    |      

## Programbeskrivelse
Applikationen består af tre dele:
1. Menu, hvor brugeren kan vælge at søge efter spiller eller hold.
2. Kommunikation med API'en for at hente relevante data.
3. Visning af data i konsollen med et overskueligt og farverigt layout (ved hjælp af `rich`-modulet).

## Rollefordeling
- Gustas: API-integration, spillerstatistikker, menu
- Cornelius: Layout, data-præsentation, README og test

## Kilder og ressourcer
- [balldontlie.io API](https://www.balldontlie.io/)
- Python-dokumentation
- `rich`-modul til flot terminaloutput

## Redegørelse for brug af AI
Vi brugte AI (ChatGPT) til at brainstorme programstruktur, forbedre synopsisen og finde gode måder at formatere output med Rich-biblioteket.

## Konklusion
Projektet løste problemet med hurtigt at få adgang til relevant NBA-data, når man f.eks. laver en parlay. Det var lærerigt at arbejde med API'er og præsentere data på en brugervenlig måde.

## Pseudokode
START

VIS "Ready, Set, Bet!" menu
VIS "1. Søg spiller"
VIS "2. Afslut"

INPUT bruger_valg

IF bruger_valg == "1":
    INPUT spiller_navn
    KALD get_player_data(spiller_navn)
    
    HVIS spiller findes:
        KALD display_player_info(data)
    ELLERS:
        VIS "Spiller ikke fundet."

ELLERS HVIS bruger_valg == "2":
    VIS "Farvel"
    AFSLUT PROGRAM

STOP
