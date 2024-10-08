import json
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

with open("results.json", "r") as file:
    data = json.load(file)

start_years = sorted(set(entry['start_jahr'] for entry in data))
anlagehorizonts = sorted(set(entry['anlagehorizont'] for entry in data))
aktie_lengths = sorted(set(entry['aktie_laenge_am_markt'] for entry in data))
renditen = sorted(set(entry['durchschnittliche_rendite'] for entry in data))


def filter_data(start_jahr, anlagehorizont, aktie_laenge, rendite):
    return [
        entry for entry in data
        if entry['start_jahr'] == start_jahr
           and entry['anlagehorizont'] == anlagehorizont
           and entry['aktie_laenge_am_markt'] == aktie_laenge
           and entry['durchschnittliche_rendite'] == rendite
    ]


def update_plot():
    start_jahr = start_year_slider.get()
    anlagehorizont = anlagehorizont_slider.get()
    aktie_laenge = aktie_length_slider.get()
    rendite = rendite_slider.get()

    filtered_data = filter_data(start_jahr, anlagehorizont, aktie_laenge, rendite)

    ax.clear()

    if not filtered_data:
        ax.plot([], [])
    else:
        years = sorted(filtered_data[0]['average_yearly_returns'].keys())
        avg_rendites = [filtered_data[0]['average_yearly_returns'][year] for year in years]
        ax.plot(years, avg_rendites, marker='o')

        overall_return = sum(entry['overall_return'] for entry in filtered_data)
        overall_return = round(overall_return, 2)
        anzahl_aktien = sum(entry['anzahl_aktien'] for entry in filtered_data)

    # Update the figure
    ax.set_title('Durchschnittliche jährliche Renditen')
    ax.set_xlabel('Jahr')
    ax.set_ylabel('Durchschnittliche Rendite (%)')
    ax.grid(True)
    canvas.draw()

    # Hier wird der Text des Labels aktualisiert
    info_label.config(
        text=f"Gesamtrendite: {overall_return}%, Anzahl Aktien: {anzahl_aktien}")


root = tk.Tk()
root.title("Datenanalyse")

# Label für Informationen über dem Plot
info_label = tk.Label(root, text="Plot Informationen", font=("Helvetica", 12))
info_label.pack()

start_year_slider = tk.Scale(root, from_=min(start_years), to=max(start_years), resolution=1, orient=tk.HORIZONTAL,
                             label="Startjahr")
start_year_slider.pack()

anlagehorizont_slider = tk.Scale(root, from_=min(anlagehorizonts), to=max(anlagehorizonts), resolution=1,
                                 orient=tk.HORIZONTAL, label="Anlagehorizont")
anlagehorizont_slider.pack()

aktie_length_slider = tk.Scale(root, from_=min(aktie_lengths), to=max(aktie_lengths), resolution=5,
                               orient=tk.HORIZONTAL, label="Bestand der Aktie")
aktie_length_slider.pack()

rendite_slider = tk.Scale(root, from_=min(renditen), to=max(renditen), resolution=0.05, orient=tk.HORIZONTAL,
                          label="Rendite")
rendite_slider.pack()

fig = Figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

update_button = tk.Button(root, text="Update Plot", command=update_plot)
update_button.pack()

root.mainloop()