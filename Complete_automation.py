import json
import pandas as pd
import yfinance as yf
import requests
import pickle
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from numpy import double

import Unternehmenslisten
import Datumsbereiche

'''
Das Skript analysiert Aktien des S&P 500 hinsichtlich Ihrer durchschnittlichen
Rendite (CAGR) über verschiedene Zeiträume und Anlagehorizonte. Es filtert
Aktien basierend auf dem Jahr, in dem sie an der Börse gelistet wurden, un einem bestimmten
Renditeziel.
Dann gibt es noch eine grafische Darstellung der jährlichen Renditen in verschiedenen
Kategorien.
'''


def adjust_for_splits(history, start_date_str, end_date_str):
    """
    Passt die historischen Daten für Aktiensplits an.
    """
    start_date = pd.to_datetime(start_date_str).tz_localize(None)
    end_date = pd.to_datetime(end_date_str).tz_localize(None)

    if 'Stock Splits' in history.columns:
        splits = history['Stock Splits'].loc[start_date:end_date]
        for date, split in splits[splits != 0].items():
            split_ratio = 1 / split
            history.loc[:date, 'Open':'Close'] *= split_ratio

    return history


def add_successful_stock(successful_stocks, filtered_histories, stock_symbol, history, start_price_all_successful_stocks, end_price_all_successful_stocks, start_jahr, end_jahr):
    successful_stocks.append(stock_symbol)
    start_date_second_time_period, end_date_second_time_period = Datumsbereiche.finde_gueltige_datumsbereiche(start_jahr, end_jahr, history)
    history = adjust_for_splits(history, start_date_second_time_period, end_date_second_time_period)
    if start_date_second_time_period is None or end_date_second_time_period is None:
        print(f"Es wurden keine Daten zu diesem Stock: {stock_symbol} gefunden")

    filtered_histories[stock_symbol] = history.loc[start_date_second_time_period:end_date_second_time_period]
    # Berechnen der durchschnittlichen Rendite der zweiten Zeitperiode
    start_price_second_time_period = filtered_histories[stock_symbol].iloc[0]['Close']
    end_price_second_time_period = filtered_histories[stock_symbol].iloc[-1]['Close']
    start_price_all_successful_stocks += start_price_second_time_period
    end_price_all_successful_stocks += end_price_second_time_period
    return successful_stocks, filtered_histories, start_price_all_successful_stocks, end_price_all_successful_stocks


def filter_successful_stocks(stocks, start_jahr, aktie_laenge_am_markt, durchschnittliche_rendite, end_jahr):
    successful_stocks = []
    filtered_histories = {}
    start_price_all_successful_stocks = 0
    end_price_all_successful_stocks = 0

    for stock_symbol in stocks:
        try:
            history = yf.Ticker(stock_symbol).history(period="max")
            history.index = history.index.tz_localize(None)
            earliest_date = history.index.min()
            earliest_year = earliest_date.year + 1
            formatted_earliest_date = earliest_date.strftime("%Y-%m-%d")
            if start_jahr - earliest_date.year < aktie_laenge_am_markt:
                continue

            start_date_first_time_period, end_date_first_time_period = Datumsbereiche.finde_gueltige_datumsbereiche(earliest_year, start_jahr - 1, history)
            if start_date_first_time_period is None or end_date_first_time_period is None:
                print(f"Es wurden keine Daten zu diesem Stock: {stock_symbol} gefunden")
                continue

            history_first_time_period = history.loc[formatted_earliest_date:end_date_first_time_period]
            if not history_first_time_period.empty:
                start_price = history_first_time_period.iloc[0]['Close']
                end_price = history_first_time_period.iloc[-1]['Close']
                if start_price > 0 and end_price > 0:
                    num_years = start_jahr - earliest_date.year
                    cagr = (end_price / start_price) ** (1 / num_years) - 1
                    if cagr >= durchschnittliche_rendite:
                        successful_stocks, filtered_histories, start_price_all_successful_stocks, end_price_all_successful_stocks = add_successful_stock(successful_stocks, filtered_histories,
                                                                                                                                                         stock_symbol, history,
                                                                                                                                                         start_price_all_successful_stocks,
                                                                                                                                                         end_price_all_successful_stocks, start_jahr,
                                                                                                                                                         end_jahr)

            else:
                print(f"Keine historischen Daten für den angegebenen Zeitraum für {stock_symbol} gefunden.")
                continue

        except Exception as e:
            print(f"Konnte keine historischen Daten für {stock_symbol} abrufen: {e}")
            continue

    return successful_stocks, filtered_histories, start_price_all_successful_stocks, end_price_all_successful_stocks


def calculate_annual_average_returns(start_jahr, end_jahr, successful_stocks, filtered_histories):
    # Initialisierung der Datenstrukturen
    annual_returns = {year: 0 for year in range(start_jahr, end_jahr)}
    stock_counts = {year: 0 for year in range(start_jahr, end_jahr)}
    start_price_yearly_successful_stocks = {year: 0 for year in range(start_jahr, end_jahr)}
    end_price_yearly_successful_stocks = {year: 0 for year in range(start_jahr, end_jahr)}

    # Berechnung der jährlichen Renditen
    for stock in successful_stocks:
        try:
            history = filtered_histories[stock]
            if history.empty:
                continue

            for year in range(start_jahr, end_jahr):
                start_date, end_date = Datumsbereiche.finde_gueltige_datumsbereiche(year, year, history)
                if start_date is None or end_date is None:
                    continue

                start_price = history['Close'].get(start_date)
                end_price = history['Close'].get(end_date)
                if start_price is None or end_price is None:
                    continue

                start_price_yearly_successful_stocks[year] += start_price
                end_price_yearly_successful_stocks[year] += end_price
                stock_counts[year] += 1

        except TypeError as e:
            print("Fehler in der for-Schleife!")
        except Exception as e:
            print(f"Konnte keine Daten für {stock} abrufen: {e}")

    # Finalisierung der Renditeberechnung
    for year in annual_returns:
        if start_price_yearly_successful_stocks[year] != 0:
            annual_returns[year] = ((end_price_yearly_successful_stocks[year] / start_price_yearly_successful_stocks[year]) - 1) * 100

    return annual_returns, stock_counts


def categorize_average_returns(annual_returns, stock_counts):
    # Kategorisierungsbereiche festlegen
    categories = list(range(-40, 80, 10))  # Von -40 % bis 70 % in 10 % Schritten
    category_counts = {cat: 0 for cat in categories}
    years_mapping = {cat: [] for cat in categories}

    # Kategorisierung der jährlichen Renditen
    for year, total_return in annual_returns.items():
        if stock_counts[year] != 0:
            print(f"Rendite für {year}: {total_return:.2f}%")
            for cat in categories:
                if cat == 70 and total_return >= cat - 5:
                    category_counts[cat] += 1
                    years_mapping[cat].append(year)
                    break
                elif cat - 5 <= total_return < cat + 5:
                    category_counts[cat] += 1
                    years_mapping[cat].append(year)
                    break
        else:
            print(f"Keine Daten für {year} gefunden.")

    return categories, category_counts, years_mapping


def calculate_total_return(start_price_all_successful_stocks, end_price_all_successful_stocks, anlagehorizont):
    total_return_all_time = None
    average_return_all_time = None

    if start_price_all_successful_stocks > 0 and end_price_all_successful_stocks > 0:
        total_return_all_time = ((end_price_all_successful_stocks / start_price_all_successful_stocks) - 1) * 100
        average_return_all_time = total_return_all_time / anlagehorizont
        print(f"Gesamtrendite über alle Jahre: {total_return_all_time:.2f}%")
        print(f"Jährliche Durchschnittsrendite über alle Jahre hinweg: {average_return_all_time:.2f}%")
    else:
        print("Keine gültigen Daten für die Berechnung der Gesamtrendite.")

    return total_return_all_time, average_return_all_time


def print_results(start_jahr, anlagehorizont, aktie_laenge_am_markt, durchschnittliche_rendite, successful_stocks, average_return_all_time):
    print("Kriterien:")
    print(f"Startjahr: {start_jahr}")
    print(f"Anlagehorizont: {anlagehorizont}")
    print(f"Aktie Länge am Markt: {aktie_laenge_am_markt}")
    print(f"Durchschnittliche Rendite: {durchschnittliche_rendite}")
    print("\nErgebnis:")
    print(f"Anzahl an Aktien, die mit den obigen Kriterien ausgewählt wurden: {len(successful_stocks)}")
    if average_return_all_time is not None:
        print(f"Durchschnittliche Rendite über den gesamten Zeitraum: {average_return_all_time:.2f}%")
    else:
        print("Durchschnittliche Rendite über den gesamten Zeitraum: Nicht verfügbar")


def show_bar_chart(categories, category_counts, years_mapping):
    labels = [f"{cat}%" for cat in categories]
    values = [category_counts[cat] for cat in categories]

    bars = plt.bar(labels, values)
    plt.xlabel('Rendite-Kategorie')
    plt.ylabel('Anzahl der Jahre')
    plt.title('Jährliche Renditen in Kategorien')

    # Hinzufügen der Jahre an jeden Balken
    for bar, cat in zip(bars, categories):
        years = years_mapping[cat]
        y_position = bar.get_height() + 0.1
        plt.text(bar.get_x() + bar.get_width() / 2, y_position, ', '.join(map(str, years)), ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()


def analyse_stocks(start_jahr, anlagehorizont, aktie_laenge_am_markt, durchschnittliche_rendite):
    end_jahr = start_jahr + anlagehorizont
    stocks = Unternehmenslisten.lese_sp500_unternehmen(start_jahr)
    successful_stocks, filtered_histories, start_price_all_successful_stocks, end_price_all_successful_stocks = filter_successful_stocks(stocks, start_jahr, aktie_laenge_am_markt,
                                                                                                                                         durchschnittliche_rendite, end_jahr)

    if successful_stocks:
        print("Folgende Aktien hatten eine durchschnittliche jährliche Rendite von 15% oder höher:")
        for stock in successful_stocks:
            print(stock)
    else:
        print("Keine Aktien gefunden, die die Kriterien erfüllen.")

    annual_returns, stock_counts = calculate_annual_average_returns(start_jahr, end_jahr, successful_stocks, filtered_histories)
    categories, category_counts, years_mapping = categorize_average_returns(annual_returns, stock_counts)
    total_return_all_time, average_return_all_time = calculate_total_return(start_price_all_successful_stocks, end_price_all_successful_stocks, anlagehorizont)
    print_results(start_jahr, anlagehorizont, aktie_laenge_am_markt, durchschnittliche_rendite, successful_stocks, average_return_all_time)
    show_bar_chart(categories, category_counts, years_mapping)

    return {'start_jahr': start_jahr, 'anlagehorizont': anlagehorizont, 'aktie_laenge_am_markt': aktie_laenge_am_markt, 'durchschnittliche_rendite': durchschnittliche_rendite,
            'average_yearly_returns': annual_returns, 'overall_yearly_return': average_return_all_time, 'overall_return': total_return_all_time, 'anzahl_aktien': len(successful_stocks)}


def main():
    # Festlegen aller möglichen Optionen
    start_jahre = list(range(2008, 2017))
    anlagehorizont_options = [5, 10, 13]
    aktie_laengen_am_markt_options = [10, 15, 20]
    durchschnittliche_renditen_options = [0.10, 0.20, 0.30, 0.50]

    # Liste zur Speicherung der Ergebnisse für jede Kombination
    results = []

    # Schleifen durch jede mögliche Kombination
    for start_jahr in start_jahre:
        for anlagehorizont in anlagehorizont_options:
            for aktie_laenge in aktie_laengen_am_markt_options:
                for rendite in durchschnittliche_renditen_options:
                    if start_jahr + anlagehorizont <= 2022:
                        result = analyse_stocks(start_jahr, anlagehorizont, aktie_laenge, rendite)
                        if result and result.get('overall_yearly_return') is not None:
                            results.append(result)
                            print(f"{result} wurde den results hinzugefügt*******************************************************************************")

    # Speichern der Ergebnisse in einer JSON-Datei
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
