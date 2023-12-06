import json
import statistics
import matplotlib.pyplot as plt

'''
    Dieser Code muss mindestens mit Python 3.8 durchgeführt werden.
    Dort sind wichtige Statistikfunktionen dazu gekommen, die in diesem Code verwendet werden.
'''


def read_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


def filter_data(data, investment_horizon, stock_duration_on_market, average_return):
    return [
        entry for entry in data
        if entry["anlagehorizont"] == investment_horizon
           and entry["aktie_laenge_am_markt"] == stock_duration_on_market
           and entry["durchschnittliche_rendite"] == average_return
    ]


def calculate_statistics(filtered_data):
    returns = [entry["overall_yearly_return"] for entry in filtered_data]
    number_of_stocks = [entry["anzahl_aktien"] for entry in filtered_data]
    return {
        "avg_rendite": sum(returns) / len(returns),
        "avg_anzahl_aktien": sum(number_of_stocks) / len(number_of_stocks),
        "std_dev_rendite": statistics.stdev(returns) if len(returns) > 1 else 0,
        "q1": statistics.quantiles(returns, n=4)[0],
        "q3": statistics.quantiles(returns, n=4)[2],
        "median": statistics.median(returns),
        "maximum": max(returns),
        "minimum": min(returns),
        "renditen": returns
    }


def create_boxplot(returns, info_text):
    plt.figure(figsize=(10, 6))
    plt.boxplot(returns)
    plt.ylabel("Returns (%)")
    plt.text(1.05, 0.5, info_text, fontsize=10, ha='left', va='center', transform=plt.gca().transAxes)
    plt.subplots_adjust(right=0.6)
    plt.show()


def process_results(data, anlagehorizonte, bestand_aktien, vorgegebene_renditen):
    results = []
    for anlagehorizont in anlagehorizonte:
        for bestand_aktie in bestand_aktien:
            for vorgegebene_rendite in vorgegebene_renditen:
                filtered_data = filter_data(data, anlagehorizont, bestand_aktie, vorgegebene_rendite)
                if filtered_data:
                    statistics = calculate_statistics(filtered_data)
                    results.append((anlagehorizont, bestand_aktie, vorgegebene_rendite, statistics))
    return results


def print_and_show_results(results):
    for result in results:
        investment_horizon, stock_duration, return_option, statistics = result
        info_text = (f"Anlagehorizont: {investment_horizon} Jahre\n"
                     f"Bestand der Aktie: {stock_duration} Jahre\n"
                     f"Vorgegebene durchschnittliche Rendite: {return_option:.2f}\n"
                     f"Durchschnittliche Rendite: {statistics['avg_rendite']:.2f}\n"
                     f"Standardabweichung: {statistics['std_dev_rendite']:.2f}\n"
                     f"Durchschnittliche Anzahl an Aktien: {statistics['avg_anzahl_aktien']:.2f}\n"
                     f"Q1: {statistics['q1']:.2f}\n"
                     f"Q3: {statistics['q3']:.2f}\n"
                     f"Median: {statistics['median']:.2f}\n"
                     f"Maximum: {statistics['maximum']:.2f}\n"
                     f"Minimum: {statistics['minimum']:.2f}")
        create_boxplot(statistics["renditen"], info_text)


# Main Program
filename = 'results.json'
data = read_data(filename)
investment_horizon_options = [5, 10, 13]
stock_durations_on_market_options = [10, 15, 20]
average_return_options = [0.10, 0.20, 0.30, 0.50]

results = process_results(data, [5, 10], stock_durations_on_market_options, average_return_options)
print_and_show_results(results)
