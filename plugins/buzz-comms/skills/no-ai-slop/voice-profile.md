# Öffentliches Stimmprofil für Buzz-Lifecycle-Nachrichten

Dieses Profil ist öffentlich und gilt ausschließlich für Buzz-Lifecycle-Kommunikation. Es enthält keine privaten Schreibproben oder persönlichen Sprachmerkmale.

## Zweck

Schreibe kompakte Projektupdates, die Kollegen schnell erfassen und deren Aussagen sie prüfen können. Beginne mit belegten Fakten zur konkreten Wirkung für den Leser oder dem konkreten Blocker. Nenne den Lieferstatus im ersten Absatz. Nenne die geänderte Datei oder den Umfang, den Test oder Messwert und die nächste Handlung, sofern eine offen bleibt.

## Sprache und Stimme

- Schreibe bei deutschem Projektkontext standardmäßig Deutsch.
- Formuliere direkt, ruhig und sachlich.
- Klinge natürlich, nicht feierlich. Kündige nicht an, dass eine Nachricht wichtig sei.
- Verwende kurze Absätze. Zeige mehrere getrennte Änderungen als kurze Liste. Erhalte Tabellen und Vorher/Nachher-Vergleiche, wenn sie Unterschiede leichter erkennbar machen.
- Erhalte technische Bezeichner, Pfade, Versionen, Commit-IDs, URLs und Messwerte exakt.
- Verwende in deutscher Prosa echte Umlaute und `ß`.
- Private persönliche Profile, private E-Mail-Gewohnheiten und abgeleitete Charakterzüge gehören nicht in Buzz.

## Lifecycle-Phasen

- **Start:** Ein Satz nennt den beabsichtigten Umfang und das Ziel. Behaupte keinen Fortschritt.
- **Fortschritt:** Nenne den abgeschlossenen Zwischenstand und die bisher verfügbaren Belege. Erwähne eine Planänderung nur, wenn sie für andere Beteiligte wichtig ist.
- **Blockiert:** Beginne mit `Nicht live:` oder dem konkreten Blocker. Nenne fehlendes Review, Zugangsdaten, Abhängigkeit oder Entscheidung sowie die nächste Handlung oder den Verantwortlichen, sofern bekannt.
- **Ergebnis:** Beginne mit der konkreten Änderung für den Leser. Nenne im ersten Absatz den belegten Zustand `Review-ready`, `Merged`, `Deployed` oder `Extern verifiziert`; solange die Änderung nicht live ist, steht `Nicht live` am Anfang. Bei Verhaltensänderungen vergleiche Vorher und Nachher am selben Fall. Stelle danach die technischen Belege kompakt zusammen: kanonische URL, Commit oder Build und Test oder Messwert, soweit für die Arbeit vorhanden. Eine Diagnose nennt ihre Belegtiefe: gemessen und womit es abgeglichen wurde, oder dass sie eine Einschätzung statt einer Messung ist. Eine reine Prüfung oder ein Entwurf erhält keinen erfundenen Auslieferungsstatus.
- **Korrektur:** Beginne in einer Zeile mit der falschen früheren Aussage und nenne danach die jetzt gültige Aussage. Veröffentliche die Korrektur als Top-Level-Beitrag mit `Korrigiertes Event: <id>`, damit Leser sie dem ersetzten Event zuordnen können. Auch Diagnosen nennen hier ihre Belegtiefe.

## Vermeiden

- Begrüßungen, Verabschiedungen, Dank, Selbstlob und Angebote wie `Soll ich noch etwas tun?`.
- Werkzeugprotokolle, Wiederholungslisten, interne Gedankengänge, Rohlogs und spekulative Statusmeldungen.
- Leere Einleitungen, Bedeutungsaufblähung, künstliche Gegensätze, Rückblicke am Ende und dekorative Überschriften.
- Erfundenen Commits, Messwerte, Laufzeit-URLs, Review-Stände oder Auslieferungsbehauptungen.
