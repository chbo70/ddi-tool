# Übersicht der Datenquellen

Wir haben uns zu Beginn alle Datenquellen aus der Publikation Ayvaz et al.[^1] mal angeschaut. Einige Quellen waren nur schwer zu erreichen und der Download war hinter einer Registrierung versteckt. Viele der Quellen waren auch ähnlich, zu der in Ihrer mitgelieferten CSV-Datein. Daher haben wir uns entschieden ein Skript zu schreiben, um das File in eine SQL Datenbank zu importieren.

Nicht alle der angeführten Datenqullen haben das gleiche Format, manche sind auch unvollständig und fehlerhaft. Es gibt zwei Arten wie die Daten angeführt werden. Einmal wird die DDI mit einem Label beschrieben und zum anderen mit einer Wahrscheinlichkeit und einer Krankheit. Daher haben wir uns dafür entschieden, zwei Tabellen zu erstellen. Die eine beinhaltet nur die Daten von Twosides, während die zweite alle restlichen Einträge zusammenfässt.

[^1]: https://doi.org/10.1016/j.jbi.2015.04.006
