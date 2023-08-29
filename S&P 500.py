import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt

url = "https://pkgstore.datahub.io/core/s-and-p-500-companies/constituents_json/data/297344d8dc0a9d86b8d107449c851cc8/constituents_json.json"  # Ersetzen Sie dies durch die tatsächliche URL des JSON

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
    for year, value in annual_return.dropna().items():
        if value < -0.4:
            returns_years_mapping[-40].append(year.year)
        elif value < -0.3:
            returns_years_mapping[-30].append(year.year)
        elif value < -0.2:
            returns_years_mapping[-20].append(year.year)
        elif value < -0.1:
            returns_years_mapping[-10].append(year.year)
        elif value < 0.0:
            returns_years_mapping[0].append(year.year)
        elif value < 0.1:
            returns_years_mapping[10].append(year.year)
        elif value < 0.2:
            returns_years_mapping[20].append(year.year)
        elif value < 0.3:
            returns_years_mapping[30].append(year.year)
        elif value < 0.4:
            returns_years_mapping[40].append(year.year)
        elif value < 0.5:
            returns_years_mapping[50].append(year.year)
        elif value < 0.6:
            returns_years_mapping[60].append(year.year)
        elif value >= 0.6:
            returns_years_mapping[60].append(year.year)
        else:
            key = int(value // 0.1 * 10) * 10
            if key in returns_years_mapping:
                returns_years_mapping[key].append(year.year)
            else:
                print(f"Unerwartete Rendite gefunden: {value * 100}% für {year.year}")

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
y = [] # [len(years) for years in returns_years_mapping.values()]

bars = plt.bar(x, y, align='center', width=8)

# Jahreszahlen auf den Balken anzeigen
for bar, years in zip(bars, returns_years_mapping.values()):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, ', '.join(map(str, years)), ha='center', va='bottom', rotation=90)

plt.xticks(x, [f"{val}%" for val in x])
plt.xlabel('Jährliche Rendite')
plt.title('Jahre für jede Renditekategorie')
plt.grid(axis='y')

# Anzeigen
plt.tight_layout()
plt.show()

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
