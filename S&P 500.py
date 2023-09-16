import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt

url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/297344d8dc0a9d86b8d107449c851cc8/constituents_json.json"

response = requests.get(url)
if response.status_code == 200:
    stocks = response.json()
else:
    print(f"Fehler beim Abrufen des JSON: {response.status_code}")

successful_stocks = []

#returns_years_mapping = {k: [] for k in range(-40, 70, 10)}

for stock in stocks:
    stock_symbol = stock["Symbol"]

    try:
        # Historische Daten für den gegebenen Zeitraum abrufen
        history = yf.Ticker(stock_symbol).history(start="2013-01-01", end="2018-01-01")
        # Jährliche Rendite berechnen
        annual_return = history['Close'].resample('Y').ffill().pct_change()

        ''' Rendite in die entsprechende Kategorie einsortieren
        for year, value in annual_return.dropna().items():
            for k in returns_years_mapping.keys():
                if k * 0.01 <= value < (k + 10) * 0.01:
                    returns_years_mapping[k].append(year.year)
                    break
        '''

        # Durchschnittliche Rendite über den Zeitraum berechnen
        average_return = annual_return.mean()
        # Stocks mit über 15% durchschnittlicher Rendite aufnehmen
        if average_return >= 0.15:
            successful_stocks.append(stock_symbol)
            print(f"{stock_symbol} der erfolgreichen Stocks hinzugefügt")
    except Exception as e:
        # Fehlermeldung ausgeben, wenn Datenabruf fehlschlägt
        print(f"Konnte keine historischen Daten für {stock_symbol} abrufen: {e}")


'''
# Balkendiagramm erstellen
x = list(returns_years_mapping.keys())
y = [len(years) for years in returns_years_mapping.values()]

bars = plt.bar(x, y, align='center', width=8)

plt.xticks(x, [f"{val}%" for val in x])
plt.xlabel('Jährliche Rendite')
plt.ylabel('Anzahl Jahre')
plt.title('Jahre für jede Renditekategorie')
plt.grid(axis='y')

plt.tight_layout()
plt.show()

for k, v in returns_years_mapping.items():
    print(f"Renditekategorie {k}%: {', '.join(map(str, v))}")
'''

if successful_stocks:
    print("Folgende Aktien hatten eine durchschnittliche jährliche Rendite von 15% oder höher:")
    for stock in successful_stocks:
        print(stock)
else:
    print("Keine Aktien gefunden, die die Kriterien erfüllen.")

# Durchschnittsrendite für jedes Jahr berechnen und drucken
annual_returns = {year: 0 for year in range(2013, 2018)}
stock_counts = {year: 0 for year in range(2013, 2018)}

#hier bin ich stehen geblieben. Es werden aktuell keine Daten von den jeweiligen stock_symbols gelesen.
# Deswegen will ich den stock erst mal printen lassen im nächsten Durchlauf und schauen, was passiert
for stock in successful_stocks:
    print(stock)
    try:
        history = yf.Ticker(stock).history(start="2013-01-01", end="2018-01-01")
        for year in range(2013, 2018):
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"

            # Die Methode asfreq gibt den letzten nicht fehlenden Wert in einem gegebenen Zeitraum zurück
            start_price = history['Close'].asfreq('D').first_valid_index()
            end_price = history['Close'].asfreq('D').last_valid_index()

            if start_price is None or end_price is None:
                print(f"Es wurden keine Daten zu diesem Stock: {stock} gefunden")
                continue

            yearly_return = (end_price / start_price) - 1
            annual_returns[year] += yearly_return
            stock_counts[year] += 1
    except Exception as e:
        print(f"Konnte keine Daten für {stock} abrufen: {e}")

for year, total_return in annual_returns.items():
    if stock_counts[year] != 0:
        average_return = total_return / stock_counts[year] * 100
        print(f"Durchschnittliche Rendite für {year}: {average_return:.2f}%")
    else:
        print(f"Keine Daten für {year} gefunden.")
