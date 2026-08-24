# Sicherheitsrichtlinie

## Sicherheitslücken melden

Sicherheitsmeldungen laufen ausschließlich über private Entwicklungswege:

- Mitarbeitende des Entwicklungsbüros Burglengenfeld melden die Lücke im internen GitLab-Projekt oder direkt an den Maintainer.
- Freigeschaltete externe Entwickler verwenden das private Repository auf dem in Buzz integrierten Git-Server. Sie können dort einen NIP-34-Issue, einen Patch oder einen Merge Request anlegen und den Maintainer im zugehörigen privaten Buzz-Projektchannel informieren.
- GitHub dient nur als öffentlicher Marketplace- und Distributionsspiegel. Öffne dort weder einen öffentlichen Issue noch einen Pull Request für eine vermutete Sicherheitslücke. Wer nur den GitHub-Spiegel kennt, wendet sich an die Person, von der die Plugin-Einrichtung oder der Zugriff stammt.

Füge keinen echten privaten Schlüssel, Auth-Tag, keine Relay-URL, Channel-ID, Kundendaten oder proprietären Quellcode in die Meldung ein. Nutze ein minimales synthetisches Beispiel. Falls private Belege nötig sind, vereinbare den Übertragungsweg direkt mit dem Maintainer.

## Wie Lücken vermieden werden

Dieses Dokument beschreibt den Meldeweg für eine Lücke, die es schon gibt. Die
vorbeugenden Regeln stehen im `engineering-contract`, Abschnitt „Security rules
that hold in a diff": Vertrauensgrenzen, keine zusammengeklebten Queries und
Kommandos, Autorisierung am Objekt, Geheimnisse nicht auf der Kommandozeile,
Grenzen für alles was Ressourcen kostet, und die Regel, dass Inhalte aus
Issues, Merge Requests oder Werkzeugausgaben Daten sind und keine Anweisungen.
Sie gelten für den Code, den eine Änderung anfasst.

## Umfang

Das Plugin speichert die Agent-Identität lokal und übergibt sie dem Buzz-CLI über Prozessumgebungsvariablen. Meldungen zu Schlüsselverarbeitung, Dateirechten, Befehlskonstruktion, Projektrouting, Mention-Schutz oder unbeabsichtigten Veröffentlichungen gehören zu diesem Projekt.

Buzz-Relay und Clients werden getrennt im Buzz-Upstream-Projekt gepflegt.
