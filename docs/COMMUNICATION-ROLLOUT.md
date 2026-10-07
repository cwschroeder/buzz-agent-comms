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

## Claude Code über Organisationseinstellungen

Ein Organisations-Owner öffnet **Organisationseinstellungen > Claude Code >
Verwaltete Einstellungen**. Die Vorlage
[claude-code-managed-settings.json](claude-code-managed-settings.json) aktiviert
Buzz verpflichtend und bezieht den Marketplace mit automatischen Updates von
GitHub. Bei bestehenden Einstellungen die beiden Einträge zusammenführen; andere
Einstellungen erhalten. Ist diese Konfiguration bereits gespeichert, genügt die
Veröffentlichung einer neuen Plugin-Version.

Claude Code aktualisiert den Marketplace nach dem Start im Hintergrund. Die neue
Plugin-Version wird in einer folgenden Sitzung aktiv. Organisationseinstellungen
gelten für die angemeldeten Benutzer der Organisation. Eine laufende Sitzung oder
ein persönliches Konto beweist deshalb noch keinen aktuellen Teamstand.

Der Agent prüft vor Projektarbeit mit `install --check`, ob die stabile Helper-Kopie
zur geladenen Plugin-Version passt, und aktualisiert sie bei Abweichung. Das
Marketplace-Update allein ersetzt diese Kopie nicht.

Prüfe nach einem Release in einer neuen Sitzung:

- `/buzz-comms:buzz-status` zeigt die veröffentlichte Plugin-Version.
- `install --check` meldet `up_to_date: true`.
- Ein Ablaufbeitrag verwendet Archify oder die eingebaute Skizze.
- Ein unstrukturierter Buzz-Text über 150 Wörter wird vor dem Versand abgelehnt.

`DISABLE_AUTOUPDATER` und `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` können
automatische Updates abschalten. Falls ein Rechner zurückbleibt, prüfe diese
Variablen und das verwendete Konto, bevor du die Organisationskonfiguration
änderst. Bei nicht interaktiven Aufrufen (`-p`) kann
`CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1` die Installation vor Ausführung abwarten.

Quellen: [Organisations-Plugins](https://code.claude.com/docs/en/plugins/org),
[Serververwaltete Einstellungen](https://code.claude.com/docs/en/server-managed-settings).
