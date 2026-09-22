# Schreibregeln gemeinsam verteilen

Die Regeln stehen im Plugin unter `skills/buzz-team-communication`, `show-me`
und `no-ai-slop`. `bro` erhält hilfreiche Gliederung. Lokale Agents verweisen auf
diese Dateien über ihren gemeinsamen Adapter; sie pflegen keine eigene Kopie
des Stimmprofils. Private E-Mail-Profile bleiben außerhalb des Plugins.

## Lokale Agents

Prüfe den tatsächlich verwendeten Konfigurationsordner, einschließlich möglicher
Umgebungsvariablen. Die üblichen Einstiegspunkte sind:

| Agent | Einstieg |
|---|---|
| Claude Code | globale `CLAUDE.md` mit Verweis auf die gemeinsamen Regeln |
| Codex | globale `AGENTS.md` mit Verweis auf den Buzz-Adapter |
| Pi | `AGENTS.md` im aktiven Agent-Verzeichnis |
| prime-agent | `AGENTS.md` oder ergänzender `APPEND_SYSTEM.md` im aktiven Agent-Verzeichnis |

Jeder Einstieg muss vor Buzz-Projektarbeit denselben Adapter laden. Der Adapter
lädt den freigegebenen Plugin-Stand und verlangt das öffentliche Stimmprofil,
den Visualisierungs-Skill und die abschließende Textprüfung. Die lokale
Helper-Syntax und Identität bleiben im Adapter.

Nach einer Aktualisierung in einer frischen Sitzung je Agent prüfen:

1. Welcher Einstieg und welcher Plugin-Pfad werden tatsächlich geladen?
2. Nennt der Agent Wirkung, Lieferstatus und einen belegten Vergleich?
3. Bleiben hilfreiche Listen und Tabellen bei einer Vereinfachung erhalten?
4. Wählt er bei fehlenden Medienwerkzeugen einen brauchbaren Text-Fallback?
5. Unterscheidet er Konzepte, lokale Tests und echte Auslieferungsnachweise?

Nutze die synthetischen Fälle aus `examples.md` als Schreibaufgaben ohne Versand.
Ein Dateiverweis beweist die Konfiguration, noch nicht das Verhalten des Agents.
Bereits laufende Sitzungen müssen die geänderten Regeln neu laden.

## Team-Plugin

Der Maintainer veröffentlicht die geprüfte Version über den vorgesehenen
öffentlichen Export. Das interne Repository wird niemals direkt in den
öffentlichen Marketplace gespiegelt. Versionsnummern in beiden Manifesten und
im Helper müssen übereinstimmen.

Nach Veröffentlichung aktualisieren Teammitglieder Marketplace und Plugin:

```text
/plugin marketplace update buzz-agent-comms
/plugin update buzz-comms@buzz-agent-comms
/reload-plugins
/buzz-comms:buzz-setup
/buzz-comms:buzz-status
```

Ein Quellcommit beweist keine Installation auf einem Kollegenrechner. Nenne im
Ergebnis getrennt den geprüften Quellstand, den veröffentlichten Stand und die
tatsächlich geprüften Installationen. Zusätzliche Grafikdienste sind optional;
das Plugin installiert sie nicht automatisch.
