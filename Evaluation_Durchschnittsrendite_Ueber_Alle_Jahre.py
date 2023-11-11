import json
import statistics

# Dateipfad der JSON-Datei
filename = 'results.json'

# Optionen für die verschiedenen Kombinationen
anlagehorizont_options = [5, 10, 13]
aktie_laengen_am_markt_options = [10, 15, 20]
durchschnittliche_renditen_options = [0.10, 0.15, 0.20]

# JSON-Datei einlesen
with open('results.json', 'r') as f:
    data = json.load(f)

# Liste zum Speichern der Ergebnisse
ergebnisse = []

# Durchschnittsberechnung und Standardabweichung für jede Kombination
for anlagehorizont in anlagehorizont_options:
    for aktie_laenge in aktie_laengen_am_markt_options:
        for rendite in durchschnittliche_renditen_options:

            # Filtern der Daten, die den aktuellen Kriterien entsprechen
            filtered_data = [
                entry for entry in data
                if entry["anlagehorizont"] == anlagehorizont
                   and entry["aktie_laenge_am_markt"] == aktie_laenge
                   and entry["durchschnittliche_rendite"] == rendite
                   and entry["overall_average_return"] is not None
            ]

            # Überprüfung, ob gefilterte Daten vorhanden sind
            if filtered_data:
                renditen = [entry["overall_average_return"] for entry in filtered_data]
                avg_rendite = sum(renditen) / len(renditen)

                # Berechnung der Standardabweichung, falls mehr als ein Datensatz vorhanden ist
                if len(renditen) > 1:
                    std_dev_rendite = statistics.stdev(renditen)
                else:
                    std_dev_rendite = 0

                # Hinzufügen der Ergebnisse zur Liste
                ergebnisse.append((
                    anlagehorizont, aktie_laenge, rendite, avg_rendite, std_dev_rendite
                ))

# Sortieren der Ergebnisse nach Standardabweichung in absteigender Reihenfolge
ergebnisse.sort(key=lambda x: x[4], reverse=False)

# Ausdrucken der sortierten Ergebnisse
for ergebnis in ergebnisse:
    anlagehorizont, aktie_laenge, rendite, avg_rendite, std_dev_rendite = ergebnis
    print(f"Anlagehorizont: {anlagehorizont}, Aktienlänge am Markt: {aktie_laenge}, Durchschnittliche Rendite: {rendite:.2f}, Durchschnitt: {avg_rendite:.2f}, Standardabweichung: {std_dev_rendite:.2f}")
