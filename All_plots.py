import json
import pickle

from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

with open('results.pkl', 'rb') as f:
    results = pickle.load(f)

print(json.dumps(results, indent=4))


def plot_best_entry_points(result_json, anlagehorizont, durchschnittliche_rendite, aktie_laenge_am_markt):
    # Beste Einstiegsmöglichkeit mit diesen Kriterien
    filtered_results = [
        r for r in result_json if r and
                                  r["anlagehorizont"] == anlagehorizont and
                                  r["durchschnittliche_rendite"] == durchschnittliche_rendite and
                                  r["aktie_laenge_am_markt"] == aktie_laenge_am_markt
    ]

    # Extrahieren der Daten für die x- und y-Achsen
    start_years = [r["start_jahr"] for r in filtered_results]
    average_returns = [r["overall_average_return"] for r in filtered_results]

    plt.scatter(start_years, average_returns, color='blue')
    plt.xlabel('Startjahr')
    plt.ylabel('Durchschnittliche Gesamtrendite (%)')
    plt.title('Beste Einstiegspunkte basierend auf der Gesamtrendite')
    plt.grid(True)

    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(1))

    plt.show()





plot_best_entry_points(results, 10, 0.2, 10)
