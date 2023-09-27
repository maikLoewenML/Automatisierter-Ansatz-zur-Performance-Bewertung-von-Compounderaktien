import pandas as pd
import yfinance as yf
import requests
import pickle
import matplotlib.pyplot as plt

import Unternehmenslisten

# Startjahr und Zeitspanne vom Benutzer abfragen
start_jahr = int(input("Bitte geben Sie das Startjahr ein (z.B. 2007): "))
zeitspanne = int(input("Bitte wählen Sie eine Zeitspanne (5, 10, 15): "))

# Überprüfen, ob die Zeitspanne gültig ist
if zeitspanne not in [5, 10, 15]:
    print("Ungültige Zeitspanne. Bitte wählen Sie 5, 10 oder 15 Jahre.")
    exit()

if start_jahr + zeitspanne > 2023:
    print("Dieser Bereich liegt noch in der Zukunft und es gibt keine Daten dafür.")
    exit()

end_jahr = start_jahr + zeitspanne

stocks = Unternehmenslisten.lese_sp500_unternehmen(start_jahr)

successful_stocks = []

for stock in stocks:
    stock_symbol = stock

    try:
        # Historische Daten für den gegebenen Zeitraum abrufen
        history = yf.Ticker(stock_symbol).history(start=f"{start_jahr}-01-02", end=f"{end_jahr}-01-02")
        # Jährliche Rendite berechnen
        annual_return = history['Close'].resample('Y').ffill().pct_change()

        # Durchschnittliche Rendite über den Zeitraum berechnen
        average_return = annual_return.mean()
        # Stocks mit über 15 % durchschnittlicher Rendite aufnehmen
        if average_return >= 0.15:
            successful_stocks.append(stock_symbol)
            print(f"{stock_symbol} der erfolgreichen Stocks hinzugefügt")
    except Exception as e:
        # Fehlermeldung ausgeben, wenn Datenabruf fehlschlägt
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
all_annual_returns = {year: [] for year in range(start_jahr, end_jahr)}
for stock in successful_stocks:
    try:
        history = yf.Ticker(stock).history(start=f"{start_jahr}-01-02", end=f"{end_jahr}-01-02")
        if history.empty:
            print(f"Keine Daten für {stock} für den angegebenen Zeitraum gefunden.")
            continue

        for year in range(start_jahr, end_jahr):
            start_date = (pd.Timestamp(f"{year}-01-01")).strftime('%Y-%m-%d')
            end_date = (pd.Timestamp(f"{year}-12-31")).strftime('%Y-%m-%d')

            if start_date in history.index and end_date in history.index:
                start_price = history.loc[start_date]['Close']
                end_price = history.loc[end_date]['Close']
                yearly_return = ((end_price - start_price) / start_price)
                all_annual_returns[year].append(yearly_return)
            else:
                print(f"Es wurden keine Daten zu diesem Stock: {stock} für das Jahr {year} gefunden")

    except Exception as e:
        print(f"Konnte keine Daten für {stock} abrufen: {e}")

# Durchschnittliche Renditen für jedes Jahr berechnen und anzeigen
average_returns = {}
for year, returns in all_annual_returns.items():
    if returns:
        average_return = sum(returns) / len(returns) * 100
        average_returns[year] = average_return
        print(f"Durchschnittliche Rendite für {year}: {average_return:.2f}%")
    else:
        print(f"Keine Daten für {year} gefunden.")

categories = list(range(-40, 80, 10))  # Von -40 % bis 70 % in 10 % Schritten
category_counts = {cat: 0 for cat in categories}
years_mapping = {cat: [] for cat in categories}

for year, average_return in average_returns.items():
    for cat in categories:
        if cat == 70 and average_return >= cat - 5:  # Für Werte, die 70 % oder mehr sind
            category_counts[cat] += 1
            years_mapping[cat].append(year)  # Jahr zur Kategorie hinzufügen
            break
        if cat - 5 <= average_return < cat + 5:
            category_counts[cat] += 1
            years_mapping[cat].append(year)  # Jahr zur Kategorie hinzufügen
            break

overall_average_return = sum(average_returns.values()) / len(average_returns)
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
