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
- Weist häufige ASCII-Umschreibungen wie `fuer`, `fuenf`, `Naechster` und
  `Buendel` vor dem Senden ab. Code-formatierte Bezeichner und Pfade, URLs und
  zitierter Quelltext bleiben davon ausgenommen.
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
- Eine eigene Buzz-Human-Identität, die am selben Relay als Mitglied eingetragen
  ist. Verlangt der Relay Mitgliedschaft, trägt der Owner sie ein, bevor die
  Agent-Identität erzeugt wird (siehe „Runbook für den Buzz-Owner")

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

### 1. Relay-Zugang

Der Agent-Key bringt keine eigene Mitgliedschaft mit. Er authentifiziert sich
über die NIP-OA-Attestierung an den eigenen Buzz-Key, also muss dieser Key am
Ziel-Relay Mitglied sein. Buzz Desktop zeigt ihn in den Profil-Einstellungen
unter „Public key".

Wer das Relay schon mit dem eigenen Buzz-Client benutzt, ist Mitglied und
überspringt diesen Schritt. Sonst geht der eigene öffentliche Schlüssel an den
Buzz-Owner, der ihn einträgt. Ohne diese Aufnahme scheitert schon Schritt 3 mit
`relay_membership_required`; der Helper wiederholt in seiner Fehlermeldung, was
zu tun ist.

### 2. Konfiguration

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

### 3. Agent-Identität

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

### 4. Channel-Zugang

Der Buzz-Administrator fügt den öffentlichen Agent-Key als Mitglied der
benötigten Channels hinzu. Das Plugin erwartet standardmäßig den Channelnamen
`<repo-id>-agent`.

### 5. Projekt registrieren

Im Projekt-Checkout:

```bash
~/.config/buzz-agent/bin/project-buzz register <repo-id>
~/.config/buzz-agent/bin/project-buzz doctor
```

Bei abweichender Channel-Namenskonvention kann die UUID explizit mit
`--channel <uuid>` angegeben werden.

## Runbook für den Buzz-Owner

Die Einrichtung hat zwei Seiten. Der Kollege richtet Helper, Konfiguration und
Agent-Identität ein. Der Owner nimmt zweimal auf: einmal am Relay für den
Human-Key, einmal je Projektkanal für den Agent-Key.

### 1. Relay-Mitgliedschaft für den Human-Key

Nötig, wenn der Relay mit `BUZZ_REQUIRE_RELAY_MEMBERSHIP=true` läuft. Damit der
attestierte Agent-Key den Zugang erben kann, muss zusätzlich
`BUZZ_ALLOW_NIP_OA_AUTH=true` gesetzt sein. `buzz-admin` greift direkt auf
Datenbank und Redis des Relays zu, läuft also auf dem Relay-Host in dessen
Umgebung:

```bash
buzz-admin add-member --pubkey <human-pubkey>
buzz-admin list-members
```

Fehlt dieser Schritt, scheitert schon `project-buzz provision` beim Kollegen mit
`relay_membership_required`.

### 2. Kanalzugang für den Agent-Key

Je Projekt, mit der eigenen Human-Identität am Relay:

```bash
buzz channels list
buzz channels add-member --channel <uuid> --pubkey <agent-pubkey> --role member
buzz channels members --channel <uuid>
```

Der Kanal heißt üblicherweise `<repo-id>-agent`. Weicht der Name ab, registriert
der Kollege das Projekt mit `register --channel <uuid>`.

### 3. Abnahme

Der Kollege führt `project-buzz doctor` aus. Der Kanal muss dort auftauchen.
Erscheint er nicht, fehlt eine der beiden Aufnahmen oder der Agent-Key im
Kanal stimmt nicht mit der lokalen Identität überein.

### Rücknahme

In umgekehrter Reihenfolge, damit kein Zwischenzustand entsteht, in dem ein
Agent noch schreiben darf:

```bash
buzz channels remove-member --channel <uuid> --pubkey <agent-pubkey>
buzz-admin remove-member --pubkey <human-pubkey>
```

Der zweite Befehl sperrt den Kollegen samt aller seiner Agenten vollständig aus.
Solange er andere Kanäle nutzt, bleibt es beim Kanalentzug.

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
Das danebenliegende `voice-profile.md` beschreibt ausschließlich den
öffentlichen Stil für Buzz-Lifecycle-Texte. Private Schreibproben und
persönliche Profile gehören nicht in dieses Repository.
