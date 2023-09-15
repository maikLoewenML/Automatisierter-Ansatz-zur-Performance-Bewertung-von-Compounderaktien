import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt

url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/297344d8dc0a9d86b8d107449c851cc8/constituents_json.json"  # Ersetzen Sie dies durch die tatsächliche URL des JSON

# gucken, ob es alten stand vom s&p 500 gibt

response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    stocks = response.json()  # Das JSON als Python-Objekt (meist ein dict oder eine Liste)
    # print(stocks)
else:
    print(f"Fehler beim Abrufen des JSON: {response.status_code}")

successful_stocks = []

# Ein Dictionary zur Speicherung der Renditen und den entsprechenden Jahren
returns_years_mapping = {k: [] for k in range(-40, 70, 10)}

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

    # Hier fügen wir die Jahreszahlen den entsprechenden Renditebereichen zu
    # anstatt liste ein set nutzen
    '''
    for year, value in annual_return.dropna().items():
        print(f"Year, Value:  {year, value}")
        if value < -0.45:
            returns_years_mapping[-40].append(year.year)
        elif -0.45 <= value < -0.35:
            returns_years_mapping[-40].append(year.year)
        elif -0.35 <= value < -0.25:
            returns_years_mapping[-30].append(year.year)
        elif -0.25 <= value < -0.15:
            returns_years_mapping[-20].append(year.year)
        elif -0.15 <= value < -0.05:
            returns_years_mapping[-10].append(year.year)
        elif -0.05 <= value < 0.05:
            returns_years_mapping[0].append(year.year)
        elif 0.05 <= value < 0.15:
            returns_years_mapping[10].append(year.year)
        elif 0.15 <= value < 0.25:
            returns_years_mapping[20].append(year.year)
        elif 0.25 <= value < 0.35:
            returns_years_mapping[30].append(year.year)
        elif 0.35 <= value < 0.45:
            returns_years_mapping[40].append(year.year)
        elif 0.45 <= value < 0.55:
            returns_years_mapping[50].append(year.year)
        elif 0.55 <= value < 0.65:
            returns_years_mapping[60].append(year.year)
        else:
            # Alle Renditen, die größer oder gleich 0.65 sind, werden hier behandelt
            returns_years_mapping[60].append(year.year)
        '''

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

# Balkendiagramm erstellen
x = list(returns_years_mapping.keys())
y = [len(years) for years in returns_years_mapping.values()]

bars = plt.bar(x, y, align='center', width=8)

plt.xticks(x, [f"{val}%" for val in x])
plt.xlabel('Jährliche Rendite')
plt.ylabel('Anzahl Jahre')
plt.title('Jahre für jede Renditekategorie')
plt.grid(axis='y')

# Anzeigen
plt.tight_layout()
plt.show()

# Jahreszahlen für jede Renditekategorie ausgeben
for k, v in returns_years_mapping.items():
    print(f"Renditekategorie {k}%: {', '.join(map(str, v))}")

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
        cagr = ((end_price / start_price) ** (1 / 14)) - 1

        # Rendite zur Gesamtsumme hinzufügen
        sum_returns += cagr

    except Exception as e:
        print(f"Konnte keine aktuellen Daten für {stock} abrufen: {e}")

# Durchschnittsrendite in Prozent berechnen
average_cagr = sum_returns / len(successful_stocks) * 100
print(f"Die durchschnittliche jährliche Rendite für alle erfolgreichen Aktien von 2009 bis heute beträgt {average_cagr:.2f}%.")

# Dictionary, um die jährlichen Renditen für alle erfolgreichen Aktien zu speichern
annual_returns_per_year = {}

# Ein Dictionary, das die kumulative jährliche Rendite für jedes Jahr speichert
cumulative_annual_returns = {}

# Durchgehen jedes Jahres von 2009 bis heute
for year in range(2009, 2023 + 1):
    annual_return_for_all_stocks = 0
    num_stocks = 0

    for stock in successful_stocks:
        try:
            # Historische Daten für das aktuelle Jahr abrufen
            history = yf.Ticker(stock).history(start=f"{year}-01-01", end=f"{year+1}-01-01")
            if not history.empty:
                start_price = history['Close'].iloc[0]  # Startpreis für das Jahr
                end_price = history['Close'].iloc[-1]   # Endpreis für das Jahr

                # Jährliche Rendite für diese Aktie für das Jahr berechnen
                annual_return = (end_price / start_price) - 1

                # Rendite zur Gesamtrendite für das Jahr hinzufügen
                annual_return_for_all_stocks += annual_return
                num_stocks += 1

        except Exception as e:
            print(f"Konnte keine Daten für {stock} für das Jahr {year} abrufen: {e}")

    # Durchschnittliche jährliche Rendite für alle Aktien für das Jahr berechnen
    if num_stocks:
        avg_annual_return = annual_return_for_all_stocks / num_stocks
        cumulative_annual_returns[year] = avg_annual_return

for year, avg_return in cumulative_annual_returns.items():
    print(f"Jahr {year}: Durchschnittliche jährliche Rendite für alle erfolgreichen Aktien: {avg_return*100:.2f}%")
