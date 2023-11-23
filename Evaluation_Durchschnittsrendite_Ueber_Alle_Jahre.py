import json
import statistics
import matplotlib.pyplot as plt

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

import matplotlib.pyplot as plt

def erstelle_boxplot(renditen, anlagehorizont, aktie_laenge_am_markt, vorgabe_durchschnittliche_rendite, durchschnitt, standardabweichung, anzahl_aktien, q1, q3, median, maximum, minimum):
    plt.figure(figsize=(10, 6))
    plt.boxplot(renditen)
    plt.ylabel("Renditen (%)")

    # Setzen des Y-Achsen-Bereichs von 0% bis 120%
    # plt.ylim(0, 120) --> bessere Vergleichbarkeit zwischen den einzelnen Boxplots. Allerdings sehen dann einige sehr "gequetscht" aus

    # Werte auf zwei Nachkommastellen runden
    durchschnitt = round(durchschnitt, 2)
    standardabweichung = round(standardabweichung, 2)
    anzahl_aktien = round(anzahl_aktien, 2)
    q1 = round(q1, 2)
    q3 = round(q3, 2)
    median = round(median, 2)
    maximum = round(maximum, 2)
    minimum = round(minimum, 2)

    info_text = (f"Anlagehorizont: {anlagehorizont} Jahre\n"
                 f"Aktienlänge am Markt: {aktie_laenge_am_markt} Jahre\n"
                 f"Vorgabe Durchschnittliche Rendite: {round(vorgabe_durchschnittliche_rendite, 2)}\n"
                 f"Durchschnitt: {durchschnitt}\n"
                 f"Standardabweichung: {standardabweichung}\n"
                 f"Durchschnittliche Anzahl an Aktien: {anzahl_aktien}\n"
                 f"Q1: {q1}\n"
                 f"Q3: {q3}\n"
                 f"Median: {median}\n"
                 f"Maximum: {maximum}\n"
                 f"Minimum: {minimum}")

    plt.text(1.05, 0.5, info_text, fontsize=10, ha='left', va='center', transform=plt.gca().transAxes)
    plt.subplots_adjust(right=0.6)
    plt.show()






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
                q1 = statistics.quantiles(renditen, n=4)[0]
                q3 = statistics.quantiles(renditen, n=4)[2]
                median = statistics.median(renditen)
                maximum = max(renditen)
                minimum = min(renditen)

                # Hinzufügen der Ergebnisse zur entsprechenden Liste
                if anlagehorizont == 5:
                    ergebnisse_5_jahre.append((anlagehorizont, aktie_laenge_am_markt, rendite, avg_rendite,
                                               std_dev_rendite, avg_anzahl_aktien, q1, q3, median, maximum, minimum, renditen))
                elif anlagehorizont == 10:
                    ergebnisse_10_jahre.append((anlagehorizont, aktie_laenge_am_markt, rendite, avg_rendite,
                                                std_dev_rendite, avg_anzahl_aktien, q1, q3, median, maximum, minimum, renditen))

        # Sortieren der Ergebnisse
        ergebnisse_5_jahre.sort(key=lambda x: (-x[3], -x[5], x[4]))
        ergebnisse_10_jahre.sort(key=lambda x: (-x[3], -x[5], x[4]))

# Ausdrucken der sortierten Ergebnisse für 5 Jahre
print("Ergebnisse für Anlagehorizont von 5 Jahren:")
for ergebnis in ergebnisse_5_jahre:
    print(
        f"Anlagehorizont: {ergebnis[0]}, Aktienlänge am Markt: {ergebnis[1]}, Durchschnittliche Rendite: {ergebnis[2]:.2f}, Durchschnitt: {ergebnis[3]:.2f}, Standardabweichung: {ergebnis[4]:.2f}, Durchschnittliche Anzahl an Aktien: {ergebnis[5]:.2f}")
    erstelle_boxplot(ergebnis[11], ergebnis[0], ergebnis[1], ergebnis[2], ergebnis[3], ergebnis[4], ergebnis[5], ergebnis[6], ergebnis[7], ergebnis[8], ergebnis[9], ergebnis[10])

# Ausdrucken der sortierten Ergebnisse für 10 Jahre
print("\nErgebnisse für Anlagehorizont von 10 Jahren:")
for ergebnis in ergebnisse_10_jahre:
    print(
        f"Anlagehorizont: {ergebnis[0]}, Aktienlänge am Markt: {ergebnis[1]}, Durchschnittliche Rendite: {ergebnis[2]:.2f}, Durchschnitt: {ergebnis[3]:.2f}, Standardabweichung: {ergebnis[4]:.2f}, Durchschnittliche Anzahl an Aktien: {ergebnis[5]:.2f}")
    erstelle_boxplot(ergebnis[11], ergebnis[0], ergebnis[1], ergebnis[2], ergebnis[3], ergebnis[4], ergebnis[5], ergebnis[6], ergebnis[7], ergebnis[8], ergebnis[9], ergebnis[10])



