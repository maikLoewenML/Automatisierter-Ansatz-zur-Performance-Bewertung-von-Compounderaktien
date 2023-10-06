import pandas as pd
import yfinance as yf
import requests
import pickle
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from numpy import double

import Unternehmenslisten

def analyse_stocks(start_jahr, anlagehorizont, aktie_laenge_am_markt, durchschnittliche_rendite):
    end_jahr = start_jahr + anlagehorizont
    if end_jahr >= 2023:
        return
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
    average_yearly_returns = {}  # Hier werden die durchschnittlichen Renditen pro Jahr gespeichert

    for year, total_return in annual_returns.items():
        if stock_counts[year] != 0:
            average_return = total_return / stock_counts[year] * 100
            average_yearly_returns[year] = average_return
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

    overall_average_return = sum(average_yearly_returns.values()) / len(average_yearly_returns)
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

    return {
        'start_jahr': start_jahr,
        'anlagehorizont': anlagehorizont,
        'aktie_laenge_am_markt': aktie_laenge_am_markt,
        'durchschnittliche_rendite': durchschnittliche_rendite,
        'average_yearly_returns': average_yearly_returns,
        'overall_average_return': overall_average_return,
        'anzahl_aktien': len(successful_stocks)
    }


# Festlegen aller möglichen Optionen
start_jahre = list(range(2008, 2023))
anlagehorizont_options = [5, 10, 15]
aktie_laengen_am_markt_options = [10, 15, 20]
durchschnittliche_renditen_options = [0.10, 0.15, 0.20]

# Liste zur Speicherung der Ergebnisse für jede Kombination
results = []

# Schleifen durch jede mögliche Kombination
for start_jahr in start_jahre:
    for anlagehorizont in anlagehorizont_options:
        for aktie_laenge in aktie_laengen_am_markt_options:
            for rendite in durchschnittliche_renditen_options:
                result = analyse_stocks(start_jahr, anlagehorizont, aktie_laenge, rendite)
                results.append(result)

# Plot der gesammelten Ergebnisse
plt.figure(figsize=(10, 6))

with open('results.pkl', 'wb') as f:
    pickle.dump(results, f)

'''
plt.xlabel("Startjahr")
plt.ylabel("Durchschnittliche Rendite über Zeitspanne (%)")
plt.title("Performance nach Startjahr und Aktienlänge am Markt")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
'''
