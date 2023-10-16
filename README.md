# Compounderaktien: Ein automatisierter Ansatz zur Performancebewertung

## Einleitung

- Investoren und Marktanalysen suchen ständig nach Wegen, ihre Anlagestrategie zu optimieren
- Könnte eine wertvolle Information sein, bo Compounder-Aktien tatsächlich im Schnitt eine überlegene Performance gegenüber dem S&P 500 ETF haben

### Kontext und Bedeutung der Compounder-Aktien im Investitionsbereich

- Compounder-Aktien sind eine wichtige Anlageklasse für Investoren, die ihr Vermögen über einen langen Zeitraum hinweg steigern möchten. Sie bieten die Möglichkeit, von der Kraft des Zinseszinses zu profitieren, da die Gewinne des Unternehmens jedes Jahr reinvestiert werden. Dies kann zu einem exponentiellen Wachstum des Unternehmenswerts führen.
- Die Bewertung der Performance von Compounder-Aktien gegenüber dem S&P 500 ist eine wichtige Aufgabe, wenn sie nach einer besseren Rendite suchen. Der S&P 500 ist ein Index, der die Performance der 500 größten Unternehmen in den USA abbildet. Die Performance von Compounder-Aktien gegenüber dem S&P 500 kann dabei helfen, zu beurteilen, ob diese Aktien alleine eine bessere Investition sind als der S&P 500 ETF.
- Ein automatisierter Ansatz kann dabei helfen, diese Aufgabe effizienter und genauer zu erledigen. Zum Einen bei der Datenerfassung, der Berechnung als auch der Visualisierung der Ergebnisse. Dies kann den Zeitaufwand für die Performancebewertung erheblich reduzieren und die Ergebnisse genauer machen.

### Zielsetzung der Arbeit

- Mehrdeutigkeit der Definiton von Compounder-Aktien analysieren
- Analyse, ob Compounder-Aktien gegenüber dem S&P 500 auf Dauer besser performen
- Identifizierung des optimalen Gleichgewichts zwischen Rendite und Risiko bei den Compounder-Aktien

### Vorgehensweise der Untersuchung

- Entwicklung eines Skripts, das automatisch eine Vielzahl von Parameterkombinationen (Dauer am Markt und jährliche Rendite) durchläuft und diejenigen Kombinationen identifiziert, die das beste Verhältnis von Rendite zu Risiko innerhalb des S&P 500 ETF bieten

## Theoretischer Rahmen

### Definition und Merkmale von Compounder-Aktien

- Aktien, die nachhaltiges und langfristiges Wachstum können
- positive Differenz zwischen der Rendite, des investierten Kapitals (ROIC) und den durchschnittlichen Kapitalkosten
  - https://www.cworldwide.com/media/s10jt2v2/the-anatomy-of-a-compounder.pdf
- es gibt relativ wenige Unternehmen, die in der Lage sind, das Vermögen der Aktionäre über die lange Frist hinweg mit überlegenen Renditen zu vermehren
- Compounders neigen dazu, in wirtschaftlichen Abschwüngen relativ robust zu sein, mit stabilen operativen Cashflows und keiner übermäßigen Verschuldung
- Qualität und Fokus des Managements
- keine häufigen CEO-Wechsel
- Compounders sind eher in Branchen zu finden, in denen relativ kapitalleichte Innovationen eine neue Nachfrage schaffen und die Preissetzungsmacht unterstützen könnte
  - https://www.morganstanley.com/im/publication/insights/investment-insights/ii_equitycompounders_en.pdf
- organisches Wachstum
- wenn der ROIC zu niedrig ist, dann muss das Unternehmen viel investieren, um das Geschäft zu erweitern
- es muss eine gute Kapitalallokation vorliegen --> vermeiden Unternehmen mit zu viel ungenutztem Bargeld in ihrer Bilanz
  - https://hedgenordic.com/2021/11/uncovering-attractively-valued-compounders/

### Überblick über den S&P 500 ETF

- Definition: Der S&P 500 (Standard & Poor's 500) ist ein Aktienindex, der die Performance von 500 großen Unternehmen an den US-Börsen abbildet und als Barometer für den US-Aktienmarkt gilt.
- Zusammensetzung: Der Index setzt sich aus Unternehmen diverser Branchen zusammen, wobei die Gewichtung auf Basis der Marktkapitalisierung erfolgt. Dies bedeutet, dass Unternehmen mit einer höheren Marktkapitalisierung (Aktienkurs mulitpliziert mit der Anzahl ausstehenden Aktien) einen größeren Einfluss auf den Index haben.
- Historie: Eingeführt im Jahr 1957, repräsentiert der S&P 500 rund 80% der gesamten US-Marktkapitalisierung und gilt al einer der besten Gesamtmarktindikatoren.
- Verwendung: Investoren und Analysten nutzen den S&P 500 oft als Benchmark, um die Performance einzelner Aktien oder Fonds mit dem Gesamtmarkt zu verlgeichen.
- ETFs & Investmentfonds: Viele Anlageprodukte wie z.B. ETFs (Exchange Traded Funds, börsengehandelte Fonds), versuchen die Performance des S&P 500 nachzubilden, um Anlegern eine einfache Möglichkeit zu bieten, am Gesamtmarkt teilzunehmen.
- Rebalancing: Um die Relevanz des Index beizubehalten, erfolgt regelmäßig ein "Rebalancing", bei dem Unternehmen auf Basis ihrer Marktkaptialisierung hinzugefügt oder entfernt werden.
  https://www.standardandpoors.com
  https://www.investopedia.com
  https://www.vanguard.com

### Relevanz von Rendite und Risiko in der Anlagestrategie

- Einführung in Rendite und Risiko:
  - Definition von Rendite: Ertrag einer Investition im Verhältnis zum investierten Kapital
  - Definition von Risiko: Unsicherheit der zukünftigen Rendite
    - Bodie, Zvi, Alex Kane, and Alan Marcus. EBOOK: Investments-Global edition. McGraw Hill, 2014.
  - Historische Renditen verschiedener Anlageklassen: Aktien, Anleihen, Rohstoffe, Immobilien
  - Risiken variieren je nach Anlageklasse und Region
    - Dimson, Elroy, Paul Marsh, and Mike Staunton. Triumph of the optimists: 101 years of global investment returns. Princeton University Press, 2002.
- Rendite-Risiko-Profil:
  - Das Rendite-Risiko-Verhältnis misst die Kompensation, die Anleger für das Eingehen eines zusätzlichen Risikos erhalten.
    - Sharpe, William F. "Mutual fund performance." The Journal of business 39.1 (1966): 119-138.
- Riskofaktoren und Compounder-Aktien:
  - Größe, Buch-Markt-Verhältnis und Momentum als gemeinsame Risikofaktoren.
  - Compounder-Aktien könnten unterschiedliche systematischen Risiken ausgesetzt sein
    - Fama, Eugene F., and Kenneth R. French. "Common risk factors in the returns on stocks and bonds." Journal of financial economics 33.1 (1993): 3-56.
- Relevanz von Rendite und Risiko für Compounder-Aktien:
  - Compounder-Aktien bieten möglicherweise höhere Renditen bei niedrigerem Risiko
- Rolle von Rendite und Risiko in der Strategieauswahl:
  - Diversifikation als Schlüssel zum Management von Rendite und Risiko.
  - Compounder-Aktien als potenzielles Instrument zur Portfolio-Optimierung
    - Bernstein, William J., and Chris Ryan. The Four Pillars of Investing: lessons for building a winning portfolio. McGraw Hill, 2010.

## Einführung in die y-finance-Bibliothek

- Was ist die y-finance Bibliothek?
  - Eine Python-Bibliothek, die einen schnellen Zugriff auf historische und aktuelle Finanzdaten ermöglicht
  - https://github.com/ranaroussi/yfinance
  - Wieso wurde sie entwickelt?
    - Antwort auf das Verschwinden von Yahoo Finance's alter API
- Grundlegende Funktionalitäten
  - Datenabfrage: Historische Daten, aktuelle Kurse
  - Integration von Pandas: Einfache Handhabung und Analyse der Daten in DataFrame-Strukturen

### Überblick und Funktionen von y-finance

- yf.Ticker():
  - Beschreibung: Erstellt ein Ticker-Objekt, das Daten für den angegebenen Aktienticker bereitstellt
  - Verwendung: Abruf eines Ticker-Objekts für eine spezifische Aktie
- .history(start="", end=""):
  - Beschreibung: Methode des Ticker-Objekts, die historische Daten zwischen den angegebenen Start- und Enddaten zurückgibt
  - Verwendung: Abruf historischer Daten zwischen einem Start- und Enddatum
- .dropna():
  - Beschreibung: Eine pandas-Methode, die Zeilen oder Spalten mit fehlenden Daten aus dem DataFrame entfernt.
  - Verwendung: Entfernen von Zeilen ohne Renditedaten.
- .items():
  - Beschreibung: Eine Methode, um Schlüssel-Wert-Paare eines Objekts (normalerweise eines Dictionarys) als Liste von Tupeln zurückzugeben.
  - Verwendung: Durchlaufen von Jahren und ihrer jeweiligen Rendite.
- .get():
  - Beschreibung: Eine Methode, um den Wert für einen gegebenen Schlüssel aus einem Objekt (normalerweise einem Dictionary oder einer Serie) abzurufen.
  - Verwendung: Abrufen von Schlusspreisen für spezifische Daten.

### Relevanz und Vorteile für Aktienanalysen

- Grundlagen der Aktienanalyse
  - Definition und Hauptzweck: Bwertung von Aktien und Vorhersage zukünftiger Preisbewegungen
    - Graham, Benjamin, et al. Security analysis: Principles and technique. Vol. 5. New York: McGraw-Hill, 1962.
  - Relevanz von Aktienanalysen
    - Bessere Investmententscheidungen durch fundierte Analysen
    - Risikominderung: Besseres Verständnis von Unternehmen und Marktbedingungen
  - Vorteile der Verwendung von y-finance für Aktienanalysen
    - Schneller Zugriff auf eine Fülle von Daten: Reduziert den Zeitaufwand für die Datenbeschaffung
    - Flexibilität: Anpassungsfähigkeit an verschiedene Analyseansätze und Analysetechniken
    - Kostenlose Nutzung der Bibliothek
    - Weitreichende Daten in die Vergangenheit

## Skript-Entwicklung und Automatisierung

- Testen der y-finance Bibliothek
- Aktuelle Unternehmensliste des S&P 500 suchen
- Filterung des Symbols dieser Unternehmensliste für alle Unternehmen
- Filterung der Unternehmen nach einer festgelegten Compounderdefinition
  - 15% durchschnittliche Rendite
  - Zeitraum 2013 - 2018
- Erstellung eines JSONs für die gefilterten Compounderaktien, da das herausfiltern zeitintensiv ist
  - diente dazu, um die weitere Entwicklung schneller voranzutreiben
- Berechnung der durchschnittlichen jährlichen Rendite für alle gefilterten Compounderaktien
- Grafische Darstellung in eine Renditekategorie, welche Jahre in diesem festgelegten Zeitraum am besten liefen
- Einbindung von Unternehmenslisten des S&P 500 seit 2007, um die Daten nicht zu verfälschen
  - mithilfe der Wayback-Maschine
- Zeitspanne für die Compounder-Definition soll in mehrere vordefinierte Bereiche geteilt werden
- Länge am Markt soll variabel berechnet werden können

### Beschreibung des zu entwickelnden Skripts unter Verwendung von y-finance

* Bibliothek und Module importieren

  * Datenmanipulation (pandas)
  * Datenabruf für Finanzdaten (yfinance)
  * Zeithandhabung (datetime, timedelta, time)
  * Visualisierung (matplotlib)
  * Weitere nützliche Tools (requests, pickle, numpy)
  * Benutzerdefinierte Module (Unternehmenslisten)
* Benutzereingabe abfragen

  * Startjahr der Analyse
  * Anlagehorizont (Dauer der Investition in Jahren)
  * Minimale Zeit, die die Aktie bereits am Markt ist
  * Durchschnittliche jährliche Rendite, die für eine Aktie erwartet wird
* Eingabevalidierung

  * Überprüfen, ob die Benutzereingaben gültig sind. Falls nicht, wird das Skript beendet
* Unternehmsndaten abrufen

  * Liste der Unternehmen im S&P 500 für das angegebene Startjahr abrufen
* Datenanalyse für jede Aktie

  * Historische Daten für jede Aktie abrufen
  * Filtern der Daten basierend auf Benutzereingaben
  * Berechnen der durschnittlichen jährlichen Rendite für jede Aktie
  * Speichern von Aktien, die die Kriterien erfüllen, in einer Liste
* Jährliche Renditen für erfolgreiche Aktien berechnen

  * Für jede erfolgreiche Aktie den jährlichen Renditeprozentsatz berechnen
  * Gesamtdurchschnitt der jährlichen Renditen berechnen
* Daten visualisieren

  * Darstellen der jährlichen Renditen in Balkendiagrammform
  * Jährliche Renditen werden in Kategorien unterteilt
  * Die Jahre werden zu den entsprechenden Balken im Diagramm hinzugefügt

#### Auswahl der Parameter

- Auswahl der Parameter konzentriert sich auf Benutzereingaben, um die Aktienanalyse zu steuern

1. Startjahr (Bestimmt den Beginn des Analysezeitraums)
2. Anlagehorizont (Legt die Dauer der Investitionsanalyse in Jahren fest)
3. Aktie Länge am Markt (Filtert Aktien aus, die nicht mindestens die angegebene Anzahl von Jahren am Markt waren)
4. Durchschnittliche Rendite (Erwartete Mindestrendite, die eine Aktie über den angegebenen Zeitraum erzielt haben sollte)

#### Filterung der Compounder-Aktien

* Ausgangsparameter festlegen
  * Nutzereingaben für Startjahr, Anlagehorizont, Aktie Länge am Markt und durchschnittliche Rendite werden abgefragt
* Initialisierung der Aktienliste
  * Die Funktion 'Unternehmenslisten.lese_sp500_unternehmen' wird verwendet, um eine Liste der S&P 500 Unternehmen für das gegebene Startjahr zu erhalten.
* Durchlaufen der Aktienliste
  * Für jede Aktie in der Liste
  * Abrufen von historischen Daten mithilfe von yf.Ticker(stock_symbol).history(period="max") werden die historischen Daten für die jeweilige Aktie abgerufen
  * Filtern nach Marktpräsenz --> die Daten der Aktie werden geprüft, um sicherzustellen, dass die Aktie für die vom Benutzer angegebene Dauer ("Aktie Länge am Markt") existiert hat.
  * Finden eines gültigen Startdatums --> für das gegebene 'start_jahr' wird versucht, ein gültiges Daten zu finden, an dem Handelsdaten für die Aktie vorliegen. Dabei wird ein Zeitraum von 10 Tagen ab dem Beginn des Jahres in Betracht gezogen (Sonntage, Feiertage werden somit ausgeschlossen)
  * Berechnung der durchschnittlichen Rendite --> die jährliche Rendite für die Aktie wird basierend auf den Schlusskursen berechnet und dann die durchschnittliche Rendite ermittelt.
  * Filtern nach Rendite --> Wenn die durchschnittliche Rendite der Aktie größer oder gleich der vom Benutzer festgelegten "durchschnittlichen Renite" ist, wird die Aktie als "erfolgreich" betrachtet und der Liste 'successful_stocks' hinzugefügt.
  * Behandlung von Ausnahmen --> Während des Prozesses werden mögliche Fehler (z.B. fehlende Daten) abgefangen und entsprechende Meldungen werden ausgegeben
  * Ergebnisausgabe --> nach Durchlauf aller Aktien werden die "erfolgreichen Aktien", also diejenigen, die die Filterkriterien erfüllt haben, ausgedruckt.
* Weitere Analyse der erfolgreichen Aktien
  * Initialisierung der Datenstrukturen --> zwei Dicitionaries ('annual_returns' und 'stock_counts' werden erstellt, um die jährlichen Renditen und die Anzahl der analysierten Aktien pro Jahr zu speichern)
  * Durchlauf der erfolgreichen Aktien
  * Für jede in 'successful_stocks' ausgeführte Aktie
  * Abrufen der historischen Daten für den Analysezeitraum --> Mithilfe von 'yf.Ticker(stock).history(start, end)' werden die historischen Daten für die Aktien im Analysezeitraum (von 'start_jahr' bis 'end_jahr') geholt.
  * Jährliche Renditeberechnung
  * Für jedes Jahr im Analysezeitraum
  * Ein gültiges Startdatum und Enddatum wird für dieses Jahr gesucht
  * Diese Daten werden verwendet, um den Start- und Endpreis der Aktie für das jeweilige Jahr zu bestimmen
  * Die jährliche Rendite wird berechnet mit: (end_price / start_price) - 1
  * Die berechnete jährliche Rendite wird zu 'annual_returns' für das entsprechende Jahr hinzugefügt und die Anzahl der analysierten Aktien für dieses Jahr wird in 'stock_counts' inkrementiert.
  * Fehlerbehandlung --> Falls während der Datenabrufung oder Ananlyse ein Fehler auftritt (z.B. fehlende Daten für ein bestimmtes Jahr), wird eine Fehlermeldung ausgegeben und mit der nächsten Aktie fortgefahren.
  * Zusammenfassung und Kategorisierung der jährlichen Renditen
  * Für jedes Jahr, für das Daten vorhanden sind
  * Die durchschnittliche Rendite wird berechnet, indem die Gesamtrendite für dieses Jahr durch die Anzahl der analysierten Aktien geteilt wird.
  * Die durchschnittliche Rendite wird dann in vorgegebene Renditekategorien (z.B. -30%, -20%, ..., 70%) eingeordnet.
  * Jedes Jahr wird der entsprechenden Renditekategorie zugeordnet.
* Darstellung der Ergebnisse
* Ein Balkendiagramm (plt.bar') wird erstellt, um die Anzahl der Jahr in jeder Renditekategorie darzustellen.
* Zu jedem Balken werden die entsprechenden Jahr als Beschriftung hinzugefügt.
* Das Diagramm wird angezeigt, um die Verteilung der durchschnittlichen Renditen über die Kategorie zu visualisieren.

#### Automatisierter Ansatz zur Datenanalyse

### Datenquellen und deren Einbindung

### Kriterien zur Bewertung von Rendite und Risiko

- Rendite
  - Historische Rendite: Dies bezieht sich auf die tatsächlich erzielte Rendite in der Vergangenheit.
- Risiko
  - Beta: Ein Maß für das systematische Risiko einer Aktie im Vergleich zum Markt. Ein Beta von 1 bedeutet, dass die Aktie sich im Allgemeinen parallel zum Markt bewegt (Sharpe, 1964) --> weitere Recherche notwendig
  - Alpha: Ein Maß für die Über- oder Unterperformance einer Anlage im Vergleich zu einem Benchmark (Jensen, 1968) --> weitere Recherche notwendig
- Diversifikation
  - Die Idee, in verschiedene Anlageklassen oder Wertpapiere zu investieren, um das Risiko zu verringern (Markowitz, 1952)

## Evaluation der Strategie

### Was sind die Kriterien für die Evaluation?

### Mehrere Zeitpunkte

## Ergebnisse

### Darstellung der automatisierten Analyseergebnisse

### Identifikation des optimalen Verhältnisses von Rendite zu Risiko

### Vergleich der Ergebnisse mit der Performance des S&P 500 ETF

### Evaluationsframework

### Verschiedene Zeiträume

## Diskussion

### Interpretation und Bewertung der Ergebnisse

### Threat of Validity

## Conclusio

### Zusammenfassung

### Weiterer Bezug von Merkmalen in die Filterung

- Einführung in die Aktienfilterung
  - Bedeutung der Datenanalyse bei der Aktienauswahl
  - Bisherige Kriterien: Startjahr, Zeitspanne, Dauer der Aktie am Markt, durchschnittliche Rendite
- Bedeutung weiterer Merkmale
  - Erweiterung des Analyse-Spektrums für eine umfassendere Bewertung
  - Möglichkeit, Risiken besser zu erkennen und Renditechancen zu optimieren
- Marktkapitalisierung
  - Ermöglicht eine Einschätzung der Größe und Stabilität eines Unternehmens
  - Unterscheidung zwischen Small, Mid und Large Caps
- Verschuldungsgrad
  - Zeigt das Verhältnis von Fremd- und Eigenkapital
  - Kann Aufschluss über die finanzielle Gesundheit und das Risikoprofil eines Unternehmens geben.
- Gewinn pro Aktie
  - Maßstab für den Ertrag, den eine Aktie generiert
  - Kann als Indikator für die Rentabilität und Wachstumspotenzial eines Unternehmens dienen.
- ROCE (Return on Capital Employed)
  - Misst die Rentabilität des eingesetzten Kapitals
  - Hilft dabei, Unternehmen zu identifizieren, die effizient Kapital einsetzen
- Weitere potenzielle Merkmale
  - Dividendenrendite, Kurs-Buchwert-Verhältnis
  - Integration weiterer Datenquellen und Analysetools
- Integration dieser Merkmale in den Analyseprozess
  - Automatisierung der Datenerfassung und Datenverarbeitung
  - Berücksichtigung dieser Merkmale bei der Aktienselektion und Aktienbewertung

#### Marktkapitalisierung

* Festlegung der Kriterien
  * Ab welcher Marktkapitalisierung ist eine Aktie eine Compounderaktie?
  * Entscheidung, ob Konzentration auf Large-Caps, Mid-Caps, Small-Caps oder eine Kombination sein soll
* Marktkapitalisierung abrufen
  * `market\_cap = ticker.info['marketCap']`
* Zusätzliche Filterbedingung abrufen
  * `if cagr >= durchschnittliche\_rendite and market\_cap >= MIN\_MARKET\_CAP:             successful\_stocks.append(stock\_symbol)`
*

#### Verschuldungsgrad

#### Gewinn pro Aktie

#### ROCE

### Weiterer Bezug von APIs für genauere Analysen

#### Weitere und spezialisierte Sektoren - Weitere ETFs, die analysiert werden könnten

### Weitere Anwendungsbereiche

## Literaturverzeichnis

## Anhänge
