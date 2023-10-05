import pandas as pd
import yfinance as yf
import requests
import pickle
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

from numpy import double

import Unternehmenslisten

# Startjahr und Zeitspanne vom Benutzer abfragen
start_jahr = int(input("Bitte geben Sie das Startjahr ein (zwischen 2008 und 2023): "))
anlagehorizont = int(input("Bitte wählen Sie eine Zeitspanne (5, 10, 15): "))
aktie_laenge_am_markt = int(input("Bitte wählen Sie eine Zeitspanne für die Länge am Markt der jeweiligen Aktie (10, "
                                  "15, 20): "))
durchschnittliche_rendite = double(input("Bitte wählen Sie die durchschnittliche Rendite der jeweiligen Aktie (0.10, "
                                         "0.12, 0.15, 0.20): "))

if anlagehorizont not in [5, 10, 15]:
    print("Ungültige Zeitspanne. Bitte wählen Sie 5, 10 oder 15 Jahre.")
    exit()

if aktie_laenge_am_markt not in [10, 15, 20]:
    print("Ungültige Länge am Markt für die Aktie. Bitte wählen Sie 10, 15 oder 20 Jahre.")
    exit()

if durchschnittliche_rendite not in [0.12, 0.15, 0.20]:
    print("Ungültige durchschnittliche Rendite. Bitte wählen Sie 0.12, 0.15 oder 0.20 aus.")

if start_jahr + anlagehorizont > 2023:
    print("Dieser Bereich liegt noch in der Zukunft und es gibt keine Daten dafür.")
    exit()

start_time = time.time()

end_jahr = start_jahr + anlagehorizont
stocks = Unternehmenslisten.lese_sp500_unternehmen(start_jahr)
successful_stocks = []

for stock in stocks:
    stock_symbol = stock
    try:
        history = yf.Ticker(stock_symbol).history(period="max")
        earliest_date = history.index.min()
        if start_jahr - earliest_date.year < aktie_laenge_am_markt:
            continue
        # Versuchen, ein gültiges Datum bis zum `start_jahr` zu finden
        latest_date = datetime.strptime(f"{start_jahr}-01-02", "%Y-%m-%d")
        for i in range(10):
            potential_latest_date = (pd.Timestamp(f"{start_jahr}-01-02") + pd.Timedelta(days=i)).strftime(
                '%Y-%m-%d')
            if not pd.isna(history['Close'].get(potential_latest_date)):
                latest_date = potential_latest_date
                break
        print(latest_date)
        # Überprüfen, ob ein gültiges Datum gefunden wurde
        if latest_date in history.index:
            # Daten bis zum gefundenen `latest_date` filtern
            filtered_history = history.loc[:latest_date]
            annual_return = filtered_history['Close'].resample('Y').ffill().pct_change()
            average_return = annual_return.mean()
            print(f"Durchschnittliche Rendite für {stock}: {average_return}")
            if average_return >= durchschnittliche_rendite:
                successful_stocks.append(stock_symbol)
                print(f"{stock_symbol} den erfolgreichen Stocks hinzugefügt")
        else:
            print(f"Konnte kein gültiges Datum für {stock_symbol} im angegebenen Zeitraum finden.")
    except Exception as e:
        print(f"Konnte keine historischen Daten für {stock_symbol} abrufen: {e}")

# with open('successful_stocks.pkl', 'rb') as f:
#     successful_stocks = pickle.load(f)

if successful_stocks:
    print("Folgende Aktien hatten eine durchschnittliche jährliche Rendite von 15% oder höher:")
    for stock in successful_stocks:
        print(stock)
else:
    print("Keine Aktien gefunden, die die Kriterien erfüllen.")

# Durchschnittsrendite für jedes Jahr berechnen und drucken
# Liste zur Speicherung der jährlichen Renditen für alle erfolgreichen Aktien
annual_returns = {year: 0 for year in range(start_jahr, end_jahr)}
stock_counts = {year: 0 for year in range(start_jahr, end_jahr)}
for stock in successful_stocks:
    print(stock)
    try:
        history = yf.Ticker(stock).history(start=f"{start_jahr}-01-02", end=f"{end_jahr}-01-02")
        if history.empty:
            print(f"Keine Daten für {stock} für den angegebenen Zeitraum gefunden.")
            continue
        for year in range(start_jahr, end_jahr):
            start_date = None
            end_date = None
            # Suche nach gültigem start_date
            for i in range(10):
                potential_start_date = (pd.Timestamp(f"{year}-01-02") + pd.Timedelta(days=i)).strftime('%Y-%m-%d')
                if not pd.isna(history['Close'].get(potential_start_date)):
                    start_date = potential_start_date
                    break
            # Suche nach gültigem end_date
            for i in range(10):
                potential_end_date = (pd.Timestamp(f"{year}-12-31") - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
                if not pd.isna(history['Close'].get(potential_end_date)):
                    end_date = potential_end_date
                    break
            if start_date is None or end_date is None:
                print(f"Es wurden keine Daten zu diesem Stock: {stock} für das Jahr {year} gefunden")
                continue
            start_price = history['Close'].get(start_date)
            end_price = history['Close'].get(end_date)
            yearly_return = (end_price / start_price) - 1
            annual_returns[year] += yearly_return
            stock_counts[year] += 1
    except TypeError as e:
        print("Fehler in der for-schleife!")
    except Exception as e:
        print(f"Konnte keine Daten für {stock} abrufen: {e}")

categories = list(range(-40, 80, 10))  # Von -40 % bis 70 % in 10 % Schritten
category_counts = {cat: 0 for cat in categories}
years_mapping = {cat: [] for cat in categories}
average_returns = {}

for year, total_return in annual_returns.items():
    if stock_counts[year] != 0:
        average_return = total_return / stock_counts[year] * 100
        average_returns[year] = average_return
        print(f"Durchschnittliche Rendite für {year}: {average_return:.2f}%")
        for cat in categories:
            if cat == 70 and average_return >= cat - 5:  # Für Werte, die 70 % oder mehr sind
                category_counts[cat] += 1
                years_mapping[cat].append(year)  # Jahr zur Kategorie hinzufügen
                break
            if cat - 5 <= average_return < cat + 5:
                category_counts[cat] += 1
                years_mapping[cat].append(year)  # Jahr zur Kategorie hinzufügen
                break
    else:
        print(f"Keine Daten für {year} gefunden.")

overall_average_return = sum(average_returns.values()) / len(average_returns)

print("Kriterien:")
print(f"Startjahr: {start_jahr}")
print(f"Anlagehorizont: {anlagehorizont}")
print(f"Aktie Länge am Markt: {aktie_laenge_am_markt}")
print(f"Durchschnittliche Rendite: {durchschnittliche_rendite}")
print("\nErgebnis:")
print(f"Anzahl an Aktien, die mit den obigen Kriterien ausgewählt wurden: {len(successful_stocks)}")
print(f"Durchschnittliche Rendite über den gesamten Zeitraum: {overall_average_return:.2f}%")

labels = [f"{cat}%" for cat in categories]
values = [category_counts[cat] for cat in categories]

bars = plt.bar(labels, values)
plt.xlabel('Rendite-Kategorie')
plt.ylabel('Anzahl der Jahre')
plt.title('Jährliche Renditen in Kategorien')

# Hinzufügen der Jahre an jeden Balken
for bar, cat in zip(bars, categories):
    years = years_mapping[cat]
    # Jahre in einen String konvertieren und am Balken anzeigen
    y_position = bar.get_height() + 0.1
    plt.text(bar.get_x() + bar.get_width() / 2, y_position,
             ', '.join(map(str, years)), ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Das Skript hat {minutes} Minuten und {seconds} Sekunden gedauert.")
