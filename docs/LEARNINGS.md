# Learnings

Dauerhaftes Gedächtnis dieses Projekts. Eine Zeile pro Erkenntnis, datiert, mit
dem Agenten, der sie gemacht hat. Append-only: Korrekturen werden angehängt und
benennen den Eintrag, den sie richtigstellen. Nichts wird gelöscht.

## 2026-08-28 - Warum Reflect ohne Hook ausgeliefert wird

- (claude) Ein `Stop`-Hook, der `{"continue": true, "prompt": "..."}` ausgibt,
  bewirkt nichts. Die Hook-Ausgabe kennt kein Feld `prompt`, und `continue:
  true` ist ohnehin der Normalfall. Wer aus einem Hook heraus etwas an das
  Modell zurückgeben will, nutzt `hookSpecificOutput.additionalContext` oder
  `decision: "block"` mit `reason`. Ein solcher Hook läuft ohne Fehlermeldung
  und sieht deshalb funktionsfähig aus.
- (claude) `Stop` feuert nach jeder Antwort, nicht am Ende einer Sitzung, und
  `SessionEnd` kann dem Modell nichts mehr zurückgeben. Eine automatische
  Reflexion am Sitzungsende gibt es im Hook-Modell also nicht, nur eine nach
  jeder einzelnen Antwort. Deshalb liefert das Plugin `/buzz-comms:reflect`
  ausschließlich von Hand aufrufbar aus, ohne Hook und ohne
  Konfigurationsdatei.
- (claude) Die Version steht an vier Stellen: `HELPER_VERSION` in
  `scripts/project-buzz`, `version` in `plugin.json` sowie `metadata.version`
  und `plugins[0].version` in `marketplace.json`. Der Test
  `test_helper_version_matches_both_manifests` vergleicht alle drei gegen die
  Helper-Konstante.

## 2026-08-31 - Ein Vertrag darf nur nennen, was er auch liefert

- (claude) `buzz-team-communication` schrieb `c4-model-skill` und
  `arc42-documentation` als Eigentümer von `docs/ARCHITECTURE.md` vor, ohne
  beide auszuliefern. Zusätzlich existiert kein Skill namens
  `c4-model-skill`; er heißt `c4-model`. Wer der Anweisung folgte, suchte
  einen Namen, den es nirgends gibt. Regel daraus: Ein Vertrag nennt entweder
  einen mitgelieferten Skill oder eine Voraussetzung mit Installationsweg,
  nie einen Namen ohne Bezugsquelle.
- (claude) Vor dem Vendieren prüfen, ob die lokale Kopie vollständig ist. Die
  Fassung unter den Agenten-Skills bestand nur aus `SKILL.md` und `LICENSE`,
  während die `SKILL.md` zehn Begleitdateien per `Read` einbindet. Vollständig
  lag sie an anderer Stelle. Ein Ausschnitt hätte den Fehler nur verschoben.
- (claude) Vendierte Fremd-Skills können eigene Abhängigkeiten mitbringen, die
  hier niemand hat. `arc42-documentation` verlangte einen `docs-management`-Skill
  und einen Perplexity-MCP-Server. Solche Zeilen gehören beim Vendieren
  ersetzt, und die Änderung gehört in die Herkunftsangabe.
- (claude) Das Frontmatter des vendierten `c4-model` war ungültiges YAML: die
  `description` stand unquotiert in einer Zeile und enthielt Doppelpunkte.
  `claude plugin validate` meldet das nicht, es prüft nur die Manifeste.
  Beim Vendieren jedes SKILL.md-Frontmatter einzeln gegen einen YAML-Parser
  laufen lassen, sonst registriert sich der Skill beim Kollegen womöglich nie.

## 2026-08-31 - Falle beim Nachführen des öffentlichen Spiegels

- (claude) Die Historie des GitHub-Spiegels ist mit der internen nicht
  verwandt, weil er aus Squash-Pushes entstanden ist. `git merge --squash main`
  verweigert deshalb den Dienst ("refusing to merge unrelated histories"), und
  `git restore --source=main -- .` legt die neuen Dateien nicht an, es fasst
  nur bereits bekannte Pfade an. Der Weg, der trägt: Zweig von `FETCH_HEAD`
  des öffentlichen `main`, dann `git checkout main -- .`, dann
  `git diff main --exit-code` als Beweis, dass der Baum inhaltlich identisch
  ist. Erst danach committen und mit der URL pushen.

## 2026-08-31 - Die Zeichengrenze war unsere eigene, nicht die von Buzz

- (claude) Ein Kollege meldete, sein Agent habe eine Lebenszyklus-Meldung
  wegen der 4000-Zeichen-Grenze aufgeteilt, was im Kanal unlesbar aussah. Die
  Grenze stammte aus keinem Protokoll: das Relay nimmt 256 KB Inhalt pro Event
  (`crates/buzz-relay/src/handlers/ingest.rs`), die laufende NIP-11-Auskunft
  meldet `max_message_length: 524288`, und im Desktop-Client kürzt nichts den
  Nachrichtentext. Die 4000 standen nur in den beiden Helfern und kamen mit dem
  ersten Plugin-Commit ohne Begründung herein. Jetzt 16000, im Gleichschritt
  beider Seiten.
- (claude) Eine harte Grenze ohne Ausweichregel erzeugt genau diesen Schaden.
  Der Skill sagte nur „Keep messages under 4000 characters" und nichts darüber,
  was bei Überschreitung zu tun ist, also hat der Agent das Naheliegende getan
  und geteilt. Eine Grenze gehört immer zusammen mit der Anweisung, was
  stattdessen geschieht: kürzen oder anhängen, niemals über mehrere Events
  verteilen.
- (claude) Die angehobene Grenze legte sofort einen zweiten Fehler frei, den
  CI unter Windows fand: der Helfer übergab den Nachrichtentext als
  Kommandozeilenargument, und Windows bricht dort bei rund 8000 Zeichen ab
  ("The command line is too long"). Der Text geht jetzt über stdin, mit
  `--content -`, was der `buzz`-CLI seit jeher unterstützt und wortgetreu
  einliest. macOS erlaubt 1 MB Argumente, deshalb bleibt der Pilot-Helfer bei
  der Argumentform; er läuft nirgends sonst. Wer die beiden Seiten angleichen
  will, muss die stille Zeilenumbruch-Falle beachten: eine Bash-Here-String
  hängt ein Newline an und verändert damit den veröffentlichten Text.
- (claude) Eine Grenze anzuheben heißt, den Weg dahinter neu zu prüfen. Der
  alte Wert hatte den Argument-Fehler acht Monate lang verdeckt.
