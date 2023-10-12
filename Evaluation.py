import json

# Dateipfad der JSON-Datei
filename = 'results.json'

# Optionen für die verschiedenen Kombinationen
anlagehorizont_options = [5, 10, 13]
aktie_laengen_am_markt_options = [10, 15, 20]
durchschnittliche_renditen_options = [0.10, 0.15, 0.20]

# JSON-Datei einlesen
with open('results.json', 'r') as f:
    data = json.load(f)

# Durchschnittsberechnung für jede Kombination
for anlagehorizont in anlagehorizont_options:
    for aktie_laenge in aktie_laengen_am_markt_options:
        for rendite in durchschnittliche_renditen_options:

            # Filtern der Daten, die den aktuellen Kriterien entsprechen
            filtered_data = [
                entry for entry in data
                if entry["anlagehorizont"] == anlagehorizont
                   and entry["aktie_laenge_am_markt"] == aktie_laenge
                   and entry["durchschnittliche_rendite"] == rendite
            ]

            # Berechnung des Durchschnitts der durchschnittlichen Renditen für den gefilterten Datensatz
            if filtered_data:
                avg_rendite = sum(entry["overall_average_return"] for entry in filtered_data) / len(filtered_data)
                print(
                    f"Anlagehorizont: {anlagehorizont}, Aktienlänge am Markt: {aktie_laenge}, Durchschnittliche Rendite: {rendite:.2f}, Durchschnitt: {avg_rendite:.2f}")
            else:
                print(
                    f"Anlagehorizont: {anlagehorizont}, Aktienlänge am Markt: {aktie_laenge}, Durchschnittliche Rendite: {rendite:.2f}, Keine Daten gefunden.")
