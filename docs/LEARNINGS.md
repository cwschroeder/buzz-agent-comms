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
