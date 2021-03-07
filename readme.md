# This is a Readme


-> we should include something about wheelchair
1. Maby Networkanlysis with streets having good tags interupted/blocked by streets with bad tags (sideway !seperate, highway=stairs, bicycle=no)
2. share not tagged vs good tagged & bad tagged -> linegraph maby

https://automating-gis-processes.github.io/site/notebooks/L6/network-analysis.html


## Endgoal:

### Analyse
1. Wheelchair = yes/no/partial zählen, Anteil davon letztes Jahr hinzugekommen ausrechnen.Punktdaten/POI
2. Qualitätsmaße pro Straße. Wheelchairrelevante Tags pro Straße, aus guten bzw schlechten Maßen errechnet sich Score, manche sollten komplett als Ausschlussmerkmal gelten (e.g. highway=stairs).
3. Anteil von guten zu schlechten/nicht passablen Straßen

### Darstellung
1. Output Graph über Zeit und ein Wert. Punkte auf Karte mit Farbe der Accessability
2. und 3. Kreisdiagramm mit Werteverteilung, Farben nach Qualität auf Straße, evtl nie nicht passablen Straßen zusätzlich als Punkt -> Rotes Kreuz für nicht passabel

#### Python Modul
Input:

-> Geojson pboly

Output:

1. Straßen Geojson mit Spalte für Qualität, Wert -1 für impassable ansonsten Wertebereich 0 bis 1. Spalte für Anteil getaggete relevante Attribute.
2. Punktdaten Geojson impassable Streets 
3. Json Qualitätsbereiche -1:Value, dann in 0.1er Schritten:Value
4. Punktdaten Geojson abfragen und mit Wheelchair tag droppen
5. Json Anteil yes, anteil no, Anteil Partial, (Anteil nicht getagged)

#### Javascript

Userinput: Bpoly upload -> per api an python modul

Useroutput: Alles graphisch dargestellt -> Karte, Kennzahlen und Graphiken.
