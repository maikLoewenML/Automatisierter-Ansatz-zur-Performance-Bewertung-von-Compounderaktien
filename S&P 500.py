import pandas as pd
import yfinance as yf
import requests

url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/297344d8dc0a9d86b8d107449c851cc8/constituents_json.json"  # Ersetzen Sie dies durch die tatsächliche URL des JSON

response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    stocks = response.json()  # Das JSON als Python-Objekt (meist ein dict oder eine Liste)
    # print(stocks)
else:
    print(f"Fehler beim Abrufen des JSON: {response.status_code}")

successful_stocks = []

for stock in stocks:
    name = stock["Name"]
    sector = stock["Sector"]
    stock_symbol = stock["Symbol"]
    # print(f"Name: {name}, Sektor: {sector}, Symbol: {symbol}")

    try:
        history = yf.Ticker(stock_symbol).history(start="1994-01-01", end="2009-01-01")
        history.index = pd.to_datetime(history.index)
    except Exception as e:
        print(f"Konnte keine historischen Daten für {stock_symbol} abrufen: {e}")
        continue

    annual_return = history['Close'].resample('Y').ffill().pct_change()

    total_return = 0
    years_counted = 0

    for year, value in annual_return.items():
        if pd.isna(value): continue
        total_return += value
        years_counted += 1

    if years_counted > 0:
        average_return = total_return / years_counted
        if average_return >= 0.15:
            successful_stocks.append(stock_symbol)

if successful_stocks:
    print("Folgende Aktien hatten eine durchschnittliche jährliche Rendite von 15% oder höher:")
    for stock in successful_stocks:
        print(stock)
else:
    print("Keine Aktien gefunden, die die Kriterien erfüllen.")

sum_returns = 0

for stock in successful_stocks:
    try:
        # Historische Daten von 2009 bis heute abrufen
        history = yf.Ticker(stock).history(start="2009-01-01", end="2023-08-09")
        start_price = history['Close'].iloc[0]  # Startpreis
        end_price = history['Close'].iloc[-1]   # Endpreis

        # Rendite für diese Aktie berechnen
        stock_return = end_price / start_price

        # Rendite zur Gesamtsumme hinzufügen
        sum_returns += stock_return
    except Exception as e:
        print(f"Konnte keine aktuellen Daten für {stock} abrufen: {e}")

# Durchschnittsrendite in Prozent berechnen
average_return_percentage = (sum_returns / len(successful_stocks) - 1) * 100

print(f"Die durchschnittliche Rendite für alle erfolgreichen Aktien von 2009 bis heute beträgt {average_return_percentage:.2f}%.")
