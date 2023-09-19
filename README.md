# Compounderaktien: Ein automatisierter Ansatz zur Performancebewertung gegenüber dem S&P 500

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
## Einführung in die y-finance-Bibliothek
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
## Skriptentwicklung und Automatisierung
### Beschreibung des zu entwickelnden Skripts unter Verwendung von y-finance
#### Auswahl der Parameter
#### Filterung der Compounder-Aktien
#### Automatisierter Ansatz zur Datenanalyse
### Datenquellen und deren Einbindung
### Kriterien zur Bewertung von Rendite und Risiko
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
#### Marktkapitalisierung
#### Verschuldungsgrad
#### Gewinn pro Aktie
#### ROCE
### Weiterer Bezug von APIs für genauere Analysen
#### Weitere und spezialisierte Sektoren - Weitere ETFs, die analysiert werden könnten
### Weitere Anwendungsbereiche
## Literaturverzeichnis
## Anhänge
