# Muster für anschauliche Buzz-Beiträge

Alle Fälle auf dieser Seite sind synthetische Schreibübungen. Sie belegen keine
Produkteigenschaft, Messung oder Auslieferung. Übernimm in echte Beiträge nur
geprüfte Fakten. Die Formen sind Beispiele, kein Pflichtschema für jeden Post.

## Verhaltensänderung

Gegebene Fakten: Ein Entwurf ging bei einem Verbindungsabbruch verloren. Die
vorbereitete Änderung erhält ihn. Abbruch, Wiederverbindung und erneutes Senden
wurden lokal geprüft. Die Änderung ist noch nicht live.

Unanschaulich: „Entwurfspersistenz implementiert und Recovery getestet.“

Lesbarer Entwurf:

> Nicht live: Nach einem Verbindungsabbruch bleibt der eingegebene Nachrichtentext
> mit der vorbereiteten Änderung erhalten.
>
> - Vorher musste der Text erneut eingegeben werden.
> - Nachher kann der Nutzer nach der Wiederverbindung weiterschreiben und senden.
>
> Lokal geprüft: Verbindungsabbruch, Wiederverbindung und erneutes Senden.

Ein echter Beitrag ergänzt den vorhandenen Review-Link und Commit. Ein Bildpaar
zeigt denselben Entwurf nach demselben Abbruch, jeweils mit dem alten und neuen
Stand. Gibt es keinen alten Screenshot, bleibt der Vergleich im Text.

## Ablauf oder Architektur

Gegebene Fakten: In einem vorgeschlagenen Freigabeablauf wählen Antragsteller die
zuständige Person bisher selbst. Künftig soll eine vorhandene Zuordnung sie
vorbelegen. Fehlt die Zuordnung, bleibt die manuelle Auswahl erhalten. Es ist ein
Konzept, keine implementierte Funktion.

> Konzept: Bei einem neuen Antrag soll die zuständige Person bereits ausgewählt
> sein, wenn eine Zuordnung vorliegt. Bisher wählen Antragsteller sie selbst.
>
> ```text
> Antrag anlegen → Zuordnung prüfen → Person vorbelegen → Antrag prüfen
> ```
>
> Fehlt die Zuordnung, wählt der Antragsteller die Person weiterhin selbst.

Für den Kanal wird der Ablauf als geprüftes Diagramm exportiert. Die manuelle
Auswahl erscheint als Abzweig. Die Bildunterschrift benennt die Vorbelegung und
den Ausnahmefall. „Konzept“ steht auch auf der Darstellung.

## Messbarer Unterschied

Gegebene Fakten: Dieselbe Suchanfrage wurde mit demselben Datenbestand und warmem
Cache je 20-mal gemessen. Der Median betrug vorher 1,8 Sekunden, nachher 0,7
Sekunden. Es handelt sich um einen lokalen Test, nicht um Produktionsmessungen.

> Nicht live: Die getestete Suche antwortet im lokalen Vergleich früher.
>
> | Messung | Vorher | Nachher |
> |---|---:|---:|
> | Median aus je 20 Durchläufen | 1,8 s | 0,7 s |
>
> Gleiche Suchanfrage, gleicher Datenbestand, warmer Cache. Wie sich die Änderung
> unter Produktionslast verhält, ist noch nicht geprüft.

Die Zahlen sind ausschließlich für diese Schreibübung erfunden. Ein echtes
Diagramm braucht gemessene Werte, Einheiten und dieselben Vergleichsbedingungen.

## Kleiner Zwischenstand und Blocker

Ein kleiner Zwischenstand bleibt ein Satz: „Die lokale Prüfung ist abgeschlossen;
der Test mit unterbrochener Verbindung steht noch aus.“

Ein Blocker nennt die fehlende Entscheidung: „Nicht live: Die fachliche Freigabe
für den geänderten Ablauf fehlt. Zu entscheiden ist, wer einen Antrag übernimmt,
wenn keine zuständige Person hinterlegt ist.“

Beide Beiträge brauchen weder Illustration noch künstlichen Vorher/Nachher-Teil.
