# buzz-agent-comms

Ein Claude-Code-Plugin, mit dem Coding-Agents ihren Arbeitsstand in privaten
[Buzz](https://github.com/block/buzz)-Projektchannels koordinieren und belegen.
Ein Projekt, ein Channel und eine gemeinsame Historie bleiben damit über
mehrere Entwicklerrechner und Agent-Instanzen hinweg erhalten.

Das Plugin veröffentlicht keine Projektdaten von selbst. Es gibt dem Agenten
einen verbindlichen Workflow und einen kleinen lokalen Helper für signierte,
deduplizierte Buzz-Nachrichten.

## Funktionen

- Liest vor Projektarbeit die letzten Channel-Nachrichten und berücksichtigt
  parallele Arbeit, aktive Worktrees, Review-Gates und offene Blocker.
- Veröffentlicht Start, relevante Fortschritte und genau ein belegtes Ergebnis.
- Trennt reviewbereite Arbeit klar von tatsächlich ausgeliefertem Code.
- Verlangt bei nutzersichtbaren Änderungen den Nachweis auf der kanonischen
  Runtime mit exaktem Commit oder Build.
- Postet geprüfte UI-Screenshots als sichtbare Top-Level-Anhänge und nennt deren
  Event-ID im Abschlussresultat.
- Erzwingt leserfertige, kompakte Buzz-Nachrichten mit echten deutschen
  Umlauten und ohne internes Reasoning oder Tool-Tagebücher.
- Blockiert echte Channel-Mentions, erlaubt aber technische Schreibweisen wie
  `@media`, `@types/react`, E-Mail-Adressen und At-Zeichen in Code.
- Erkennt, wenn der stabil installierte Helper hinter der Plugin-Version liegt.

## Inhalt

| Komponente | Aufgabe |
|---|---|
| `buzz-team-communication` | Verbindlicher Kommunikations- und Delivery-Proof-Workflow |
| `no-ai-slop` | Redigiert jeden Lifecycle-Text, bevor er im Kanal landet |
| `scripts/project-buzz` | Portabler Python-Helper für Identität, Routing, Lifecycle und Anhänge |
| `/buzz-comms:buzz-setup` | Geführte Einrichtung |
| `/buzz-comms:buzz-status` | Read-only Diagnose, Versions- und Channel-Check |

Der Helper benötigt nur Python 3.8 oder neuer und die Python-Standardbibliothek.

## Installation

In Claude Code:

```text
/plugin marketplace add https://github.com/cwschroeder/buzz-agent-comms.git
/plugin install buzz-comms@buzz-agent-comms
/buzz-comms:buzz-setup
```

`/buzz-comms:buzz-setup` kopiert den Helper nach
`~/.config/buzz-agent/bin/project-buzz`. Dadurch hängt die Laufzeit nicht vom
Plugin-Cache ab. Anschließend prüft dieser Befehl die Installation:

```bash
~/.config/buzz-agent/bin/project-buzz doctor
```

Nach einem Plugin-Update zeigt `/buzz-comms:buzz-status`, ob diese stabile Kopie
noch zum Plugin passt. Der zugrunde liegende Check ist:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/project-buzz" install --check
```

## Voraussetzungen

- Claude Code mit Plugin-Unterstützung
- Python 3.8 oder neuer
- Eine erreichbare Buzz-Relay-Instanz
- `buzz` für den laufenden Betrieb
- `buzz-admin` und `compute_auth_tag` für die einmalige Agent-Identität
- Eine eigene Buzz-Human-Identität am selben Relay

Buzz Desktop liefert den `buzz`-CLI auf unterstützten Plattformen als Sidecar.
Alternativ können die drei Werkzeuge aus dem Buzz-Quellbaum gebaut werden:

```bash
cargo build --release -p buzz-cli -p buzz-admin
cargo build --release -p buzz-sdk --example compute_auth_tag
```

Dieses Repository verteilt keine Buzz-Binaries.

## Identitäts- und Berechtigungsmodell

Jeder Entwickler erzeugt lokal ein eigenes Agent-Schlüsselpaar. Der Agent-Key
wird per NIP-OA an den eigenen Buzz-Human-Key attestiert. Der Human-Key wird nur
lokal für diese Signatur verwendet, weder gespeichert noch übertragen.

Der Relay muss Owner-Attestierungen für Mitglieder erlauben. Relay-Zugang und
Channel-Zugang bleiben getrennt: Ein Administrator nimmt anschließend nur den
öffentlichen Agent-Key in die gewünschten Projektchannels auf.

Der Agent-Name hat die Form `<client>.<person>`, beispielsweise
`claude.alex`. Der Helper lehnt nackte Fleet-Namen wie `claude` ab, damit
fremde Agenten nicht versehentlich einer lokalen Seat-Auswertung zugerechnet
werden.

Private Schlüssel gehören niemals in Konfigurationsbeispiele, Issues, Logs,
Buzz-Nachrichten oder Support-Anfragen.

## Einrichtung

### 1. Konfiguration

`/buzz-comms:buzz-setup` legt `~/.config/buzz-agent/config.json` an:

```json
{
  "relay_url": "https://buzz.example.org",
  "agent_name": "claude.alex",
  "buzz_bin": "buzz",
  "buzz_admin_bin": "buzz-admin",
  "auth_tag_bin": "compute_auth_tag",
  "projects": {}
}
```

### 2. Agent-Identität

Der Benutzer führt die Provisionierung selbst in einem interaktiven Terminal
aus, damit der Human-Key nicht durch die Agent-Konversation läuft:

```bash
~/.config/buzz-agent/bin/project-buzz provision \
  --display-name "Alex (Claude Code)" \
  --about "Coding agent"
```

Der Befehl gibt ausschließlich den öffentlichen Agent-Key für die Freischaltung
aus. Die Agent-Identität liegt lokal in
`~/.config/buzz-agent/identity.json` und erhält unter POSIX Modus `0600`.

### 3. Channel-Zugang

Der Buzz-Administrator fügt den öffentlichen Agent-Key als Mitglied der
benötigten Channels hinzu. Das Plugin erwartet standardmäßig den Channelnamen
`<repo-id>-agent`.

### 4. Projekt registrieren

Im Projekt-Checkout:

```bash
~/.config/buzz-agent/bin/project-buzz register <repo-id>
~/.config/buzz-agent/bin/project-buzz doctor
```

Bei abweichender Channel-Namenskonvention kann die UUID explizit mit
`--channel <uuid>` angegeben werden.

## Verbindlicher Workflow

Der Skill führt den Agenten durch diese Reihenfolge:

1. Plugin-/Helper-Drift prüfen.
2. Projekt fail-closed auflösen.
3. Die letzten 20 Channel-Nachrichten lesen und anwenden.
4. Vor Mutation oder längerer Ausführung einen Lifecycle-Start posten.
5. Nur relevante Meilensteine in demselben Thread ergänzen.
6. Änderungen proportional verifizieren.
7. Bei UI-Arbeit die kanonische Runtime in repräsentativen Viewports prüfen und
   datenschutzgeprüfte Screenshots top-level posten.
8. Genau ein Ergebnis mit URL, Commit oder Build, Tests, Screenshot-Event-ID und
   offenen Grenzen veröffentlichen.
9. Erst danach dem Benutzer final antworten.

Ist eine Änderung nur reviewbereit, noch nicht gemergt oder nicht live, meldet
der Agent `blocked` beziehungsweise ausdrücklich "Nicht live".

Für nicht visuelle Repository-Arbeit wird kein künstlicher Screenshot erzeugt.
Dann dienen Test-, Commit- und Runtime-Status als Beleg.

## Helper-Kommandos

```text
project-buzz install [--check]
project-buzz provision --display-name <name> [--about <text>]
project-buzz register <repo-id> [--path <path>] [--channel <uuid>]
project-buzz resolve [repo-id]
project-buzz context [repo-id] [limit]
project-buzz start <update-id> <text> [repo-id]
project-buzz progress <update-id> <root-event-id> <text> [repo-id]
project-buzz blocked <update-id> <root-event-id> <text> [repo-id]
project-buzz result <update-id> <root-event-id> <text> [repo-id]
project-buzz attach <update-id> <text> <files...> [--repo-id <repo-id>]
project-buzz doctor
project-buzz --version
```

Lifecycle-Posts werden anhand Phase und Update-ID dedupliziert. Anhänge werden
bewusst top-level veröffentlicht, damit sie nicht in einem eingeklappten Thread
verschwinden.

## Windows

Unter Windows den Helper nicht über seinen `python3`-Shebang starten. Das Setup
erzeugt dafür einen Launcher:

```text
python ~/.config/buzz-agent/bin/project-buzz <command>  # Git Bash
project-buzz.cmd <command>                              # cmd oder PowerShell
```

Wenn die verdeckte Schlüsselabfrage unter Git Bash wegen mintty nicht erscheint,
den Provisionierungsbefehl aus cmd oder PowerShell starten oder `winpty`
verwenden. Die POSIX-Modusprüfung der Identitätsdatei ist unter Windows
deaktiviert; dort schützen die ACLs des Benutzerprofils die Datei.

## Datenschutz und öffentliche Beiträge

Vor jedem Screenshot-Upload müssen Zugangsdaten, private Personen- oder
Kundendaten, interne URLs und sensibler Browser-Chrome ausgeschlossen oder
maskiert werden. Geschäftsdaten dürfen nicht eigens für einen schöneren
Screenshot erfunden werden.

Bitte keine realen Relay-URLs, Channel-UUIDs, Public Keys, Auth-Tags, lokale
Identitätsdateien oder proprietären Projektinhalte in Issues und Pull Requests
einfügen. Verwende reduzierte, synthetische Beispiele.

Sicherheitsprobleme bitte privat über GitHub Security Advisories melden, siehe
[SECURITY.md](SECURITY.md).

## Entwicklung und Tests

```bash
python -m py_compile plugins/buzz-comms/scripts/project-buzz
python -m unittest discover -s plugins/buzz-comms/tests
```

Die Tests benötigen keinen Relay und verwenden einen lokalen Fake-CLI. Sie
prüfen unter anderem Markerformat, Routing, Mention-Schutz, Versionsdrift,
Deduplication, Anhänge und Dateirechte.

## Lizenz

[MIT](LICENSE)

Der mitgelieferte Skill `no-ai-slop` stammt von Peter Yang und steht ebenfalls
unter MIT. Seine Lizenzdatei liegt unverändert neben dem Skill unter
`plugins/buzz-comms/skills/no-ai-slop/LICENSE` und gehört zu jeder Kopie.
