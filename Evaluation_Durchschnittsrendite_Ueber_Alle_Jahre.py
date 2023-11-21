import json
import statistics

# Dateipfad der JSON-Datei
filename = 'results.json'

# Optionen für die verschiedenen Kombinationen
anlagehorizont_options = [5, 10, 13]
aktie_laengen_am_markt_options = [10, 15, 20]
durchschnittliche_renditen_options = [0.10, 0.20, 0.30, 0.50]

# JSON-Datei einlesen
with open('results.json', 'r') as f:
    data = json.load(f)

# Liste zum Speichern der Ergebnisse
ergebnisse_5_jahre = []
ergebnisse_10_jahre = []

# Durchschnittsberechnung und Standardabweichung für jede Kombination
for anlagehorizont in [5, 10]:  # Beschränkung auf 5 und 10 Jahre
    for aktie_laenge_am_markt in aktie_laengen_am_markt_options:
        for rendite in durchschnittliche_renditen_options:
            filtered_data = [
                entry for entry in data
                if entry["anlagehorizont"] == anlagehorizont
                   and entry["aktie_laenge_am_markt"] == aktie_laenge_am_markt
                   and entry["durchschnittliche_rendite"] == rendite
            ]

            # Überprüfen, ob gefilterte Daten vorhanden sind
            if filtered_data:
                renditen = [entry["overall_average_return"] for entry in filtered_data]
                anzahl_aktien_liste = [entry["anzahl_aktien"] for entry in filtered_data]
                avg_rendite = sum(renditen) / len(renditen)
                avg_anzahl_aktien = sum(anzahl_aktien_liste) / len(anzahl_aktien_liste)

                # Berechnung der Standardabweichung, falls mehr als ein Datensatz vorhanden ist
                std_dev_rendite = statistics.stdev(renditen) if len(renditen) > 1 else 0

                # Hinzufügen der Ergebnisse zur entsprechenden Liste
                if anlagehorizont == 5:
                    ergebnisse_5_jahre.append((anlagehorizont, aktie_laenge_am_markt, rendite, avg_rendite,
                                               std_dev_rendite, avg_anzahl_aktien))
                elif anlagehorizont == 10:
                    ergebnisse_10_jahre.append((anlagehorizont, aktie_laenge_am_markt, rendite, avg_rendite,
                                                std_dev_rendite, avg_anzahl_aktien))

        # Sortieren der Ergebnisse
        ergebnisse_5_jahre.sort(key=lambda x: (-x[3], -x[5], x[4]))
        ergebnisse_10_jahre.sort(key=lambda x: (-x[3], -x[5], x[4]))

# Ausdrucken der sortierten Ergebnisse für 5 Jahre
print("Ergebnisse für Anlagehorizont von 5 Jahren:")
for ergebnis in ergebnisse_5_jahre:
    print(
        f"Anlagehorizont: {ergebnis[0]}, Aktienlänge am Markt: {ergebnis[1]}, Durchschnittliche Rendite: {ergebnis[2]:.2f}, Durchschnitt: {ergebnis[3]:.2f}, Standardabweichung: {ergebnis[4]:.2f}, Durchschnittliche Anzahl an Aktien: {ergebnis[5]:.2f}")

# Ausdrucken der sortierten Ergebnisse für 10 Jahre
print("\nErgebnisse für Anlagehorizont von 10 Jahren:")
for ergebnis in ergebnisse_10_jahre:
    print(
        f"Anlagehorizont: {ergebnis[0]}, Aktienlänge am Markt: {ergebnis[1]}, Durchschnittliche Rendite: {ergebnis[2]:.2f}, Durchschnitt: {ergebnis[3]:.2f}, Standardabweichung: {ergebnis[4]:.2f}, Durchschnittliche Anzahl an Aktien: {ergebnis[5]:.2f}")
