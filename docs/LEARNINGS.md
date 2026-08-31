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
