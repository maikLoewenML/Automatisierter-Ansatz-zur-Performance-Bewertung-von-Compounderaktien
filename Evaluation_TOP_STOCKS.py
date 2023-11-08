import json

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
    stocks = Unternehmenslisten.lese_sp500_unternehmen(start_jahr)
    successful_stocks = []
    stocks_cagr = {}
    filtered_histories = {}

    for stock in stocks:
        stock_symbol = stock
        try:
            history = yf.Ticker(stock_symbol).history(period="max")
            earliest_date = history.index.min()
            if start_jahr - earliest_date.year < aktie_laenge_am_markt:
                continue

            start_date = None
            end_date = None
            # Suche nach gültigem start_date
            for i in range(10):
                potential_start_date = (pd.Timestamp(f"{start_jahr}-01-02") + pd.Timedelta(days=i)).strftime('%Y-%m-%d')
                if not pd.isna(history['Close'].get(potential_start_date)):
                    start_date = potential_start_date
                    break
            # Suche nach gültigem end_date
            for i in range(10):
                potential_end_date = (pd.Timestamp(f"{end_jahr}-12-31") - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
                if not pd.isna(history['Close'].get(potential_end_date)):
                    end_date = potential_end_date
                    break
            if start_date is None or end_date is None:
                print(f"Es wurden keine Daten zu diesem Stock: {stock} gefunden")
                continue

            # Filtern der Daten für den gegebenen Zeitraum
            filtered_history = history.loc[start_date:end_date]

            if not filtered_history.empty:
                filtered_histories[stock_symbol] = filtered_history
                start_price = filtered_history.iloc[0]['Close']
                end_price = filtered_history.iloc[-1]['Close']
                num_years = end_jahr - start_jahr

                # Berechnung der CAGR
                cagr = (end_price / start_price) ** (1 / num_years) - 1

                print(f"CAGR für {stock}: {cagr}")
                if cagr >= durchschnittliche_rendite:
                    successful_stocks.append(stock_symbol)
                    stocks_cagr[stock_symbol] = cagr
                    print(f"{stock_symbol} den erfolgreichen Stocks hinzugefügt")
            else:
                print(f"Keine historischen Daten für den angegebenen Zeitraum für {stock_symbol} gefunden.")
        except Exception as e:
            print(f"Konnte keine historischen Daten für {stock_symbol} abrufen: {e}")

    # Sortieren der Aktien nach ihrer CAGR, in absteigender Reihenfolge
    sorted_stocks = sorted(stocks_cagr.items(), key=lambda item: item[1], reverse=True)

    # Auswahl der Top 5 Aktien
    top_5_stocks = sorted_stocks[:5]

    if top_5_stocks:
        print("Folgende TOP 5 Aktien hatten eine durchschnittliche jährliche Rendite von 15% oder höher:")
        for stock in top_5_stocks:
            print(stock)
    else:
        print("Keine Aktien gefunden, die die Kriterien erfüllen.")

    # Durchschnittsrendite für jedes Jahr berechnen und drucken
    # Liste zur Speicherung der jährlichen Renditen für alle erfolgreichen Aktien
    annual_returns = {year: 0 for year in range(start_jahr, end_jahr)}
    stock_counts = {year: 0 for year in range(start_jahr, end_jahr)}
    for stock in top_5_stocks:
        print(stock)
        stock_symbol = stock[0]
        try:
            history = filtered_histories[stock_symbol]
            if history.empty:
                print(f"Keine Daten für {stock} für den angegebenen Zeitraum gefunden.")
                continue
            for year in range(start_jahr, end_jahr):
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

    # Berechnung der durchschnittlichen Rendite über alle Jahre hinweg
    total_returns_all_time = 0
    total_stock_counts_all_time = 0

    for stock in top_5_stocks:
        print(stock)
        try:
            history = filtered_histories[stock_symbol]
            if history.empty:
                print(f"Keine Daten für {stock} für den angegebenen Zeitraum gefunden.")
                continue

            start_price = history.iloc[0]['Close']
            end_price = history.iloc[-1]['Close']

            # Gesamtrendite für diesen Bestand berechnen
            total_return = (end_price / start_price) - 1
            total_returns_all_time += total_return
            total_stock_counts_all_time += 1

        except Exception as e:
            print(f"Konnte keine Daten für {stock} abrufen: {e}")

    average_return_all_time = None
    # Durchschnittliche Rendite über alle Jahre hinweg berechnen
    if total_stock_counts_all_time > 0:
        average_return_all_time = (total_returns_all_time / total_stock_counts_all_time) * 100 / anlagehorizont
        print(f"Durchschnittliche Rendite über alle Jahre: {average_return_all_time:.2f}%")
    else:
        print("Keine gültigen Daten für die Berechnung der durchschnittlichen Rendite über alle Jahre.")

    print("Kriterien:")
    print(f"Startjahr: {start_jahr}")
    print(f"Anlagehorizont: {anlagehorizont}")
    print(f"Aktie Länge am Markt: {aktie_laenge_am_markt}")
    print(f"Durchschnittliche Rendite: {durchschnittliche_rendite}")
    print("\nErgebnis:")
    print(f"Anzahl an Aktien, die mit den obigen Kriterien ausgewählt wurden: {len(top_5_stocks)}")
    print("Aktiensymbole:")
    for stock in top_5_stocks:
        print(stock[0])  # stock[0] enthält das Symbol, wenn Sie eine Liste von Tupeln haben
    if average_return_all_time is not None:
        print(f"Durchschnittliche Rendite über den gesamten Zeitraum: {average_return_all_time:.2f}%")
    else:
        print("Durchschnittliche Rendite über den gesamten Zeitraum: Nicht verfügbar")

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
        'average_yearly_returns': average_returns,
        'overall_average_return': average_return_all_time,
        'anzahl_aktien': len(top_5_stocks),
        'aktien': [stock[0] for stock in top_5_stocks]
    }


# Festlegen aller möglichen Optionen
start_jahre = list(range(2008, 2017))
anlagehorizont_options = [5, 10, 13]
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
                if result:
                    results.append(result)


# Speichern der Ergebnisse in einer JSON-Datei
with open('top_5_stocks.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

