import json
import plotly.graph_objects as go

# JSON-Datei einlesen
with open('results.json', 'r') as f:
    data = json.load(f)


# Daten filtern basierend auf den Werten der Slider
def filter_data(start_jahr, anlagehorizont, aktie_laenge, rendite):
    return [
        entry for entry in data
        if entry['start_jahr'] == start_jahr
        and entry['anlagehorizont'] == anlagehorizont
        and entry['aktie_laenge_am_markt'] == aktie_laenge
        and entry['durchschnittliche_rendite'] == rendite
    ]

# Erstellen Sie ein interaktives Diagramm
fig = go.Figure()

filtered_data = filter_data(data[0]['start_jahr'], data[0]['anlagehorizont'], data[0]['aktie_laenge_am_markt'], data[0]['durchschnittliche_rendite'])
years = sorted(filtered_data[0]['average_yearly_returns'].keys())
avg_rendites = [filtered_data[0]['average_yearly_returns'][year] for year in years]
fig.add_trace(go.Scatter(x=years, y=avg_rendites, mode='lines'))

# Sliders
start_years = sorted(set(entry['start_jahr'] for entry in data))
anlagehorizonts = sorted(set(entry['anlagehorizont'] for entry in data))
aktie_lengths = sorted(set(entry['aktie_laenge_am_markt'] for entry in data))
renditen = sorted(set(entry['durchschnittliche_rendite'] for entry in data))

fig.update_layout(
    updatemenus=[
        go.layout.Updatemenu(
            type="buttons",
            showactive=True,
            y=1,
            buttons=list([
                dict(label=str(year),
                     method="restyle",
                     args=[{"x": [sorted(filter_data(year, data[0]['anlagehorizont'], data[0]['aktie_laenge_am_markt'], data[0]['durchschnittliche_rendite'])[0]['average_yearly_returns'].keys())],
                            "y": [list(filter_data(year, data[0]['anlagehorizont'], data[0]['aktie_laenge_am_markt'], data[0]['durchschnittliche_rendite'])[0]['average_yearly_returns'].values())]}]) for year in start_years
            ])
        ),
        go.layout.Updatemenu(
            type="buttons",
            showactive=True,
            y=0.9,
            buttons=list([
                dict(label=str(horizont),
                     method="restyle",
                     args=[{"x": [sorted(filter_data(data[0]['start_jahr'], horizont, data[0]['aktie_laenge_am_markt'], data[0]['durchschnittliche_rendite'])[0]['average_yearly_returns'].keys())],
                            "y": [list(filter_data(data[0]['start_jahr'], horizont, data[0]['aktie_laenge_am_markt'], data[0]['durchschnittliche_rendite'])[0]['average_yearly_returns'].values())]}]) for horizont in anlagehorizonts
            ])
        ),
        go.layout.Updatemenu(
            type="buttons",
            showactive=True,
            y=0.8,
            buttons=list([
                dict(label=str(laenge),
                     method="restyle",
                     args=[{"x": [sorted(filter_data(data[0]['start_jahr'], data[0]['anlagehorizont'], laenge, data[0]['durchschnittliche_rendite'])[0]['average_yearly_returns'].keys())],
                            "y": [list(filter_data(data[0]['start_jahr'], data[0]['anlagehorizont'], laenge, data[0]['durchschnittliche_rendite'])[0]['average_yearly_returns'].values())]}]) for laenge in aktie_lengths
            ])
        ),
        go.layout.Updatemenu(
            type="buttons",
            showactive=True,
            y=0.7,
            buttons=list([
                dict(label=str(r),
                     method="restyle",
                     args=[{"x": [sorted(filter_data(data[0]['start_jahr'], data[0]['anlagehorizont'], data[0]['aktie_laenge_am_markt'], r)[0]['average_yearly_returns'].keys())],
                            "y": [list(filter_data(data[0]['start_jahr'], data[0]['anlagehorizont'], data[0]['aktie_laenge_am_markt'], r)[0]['average_yearly_returns'].values())]}]) for r in renditen
            ])
        ),
    ]
)
