# Lifecycle-Status

Agent-Posts aus `project-buzz` tragen neben dem Zeitstempel ihre Phase:
Start, Zwischenstand, Ergebnis, Blockiert oder Korrektur. Über das ⋯-Menü
eines solchen Posts zeigt **Lifecycle-Stand anzeigen** direkt in der Zeile,
ob der Thread schon ein Ergebnis, einen Blocker oder eine Korrektur hat.

## Getting started

1. In Buzz **Settings → Plugins → Manage plugins** öffnen.
2. **Load from folder** wählen und den Ordner `buzz-app-plugins/lifecycle`
   aus diesem Repository auswählen, dann **Install plugin**.
3. Das Plugin in der Liste einschalten. Neue Installationen starten
   ausgeschaltet.
4. Einen Projektkanal öffnen: An Agent-Posts steht die Phase neben dem
   Zeitstempel.

---

## Für Beitragende

- Das Plugin gilt nur für den Desktop-Client von Buzz 1.0 (`block/buzz-app`,
  Plugin-API v1). Buzz 0.X und die Mobile-App kennen keine Plugins.
- `plugin.js` ist ein fertiges ES-Modul ohne Build-Schritt. Es nutzt nur die
  Host-Dienste `react` und `conversation` und deklariert keinen Host-Zugriff
  (keine Kommandos, keine Netzwerkadressen, keine Dateien).
- Die Phase kommt aus dem Marker in der ersten Zeile, den `project-buzz`
  schreibt. `MARKER_RE` und die Regel für offene Threads müssen zu
  `plugins/buzz-comms/scripts/project-buzz` passen;
  `plugins/buzz-comms/tests/test_buzz_app_lifecycle.py` prüft beides gegen den
  Helper (braucht `node`).
- Den Thread liest das Plugin erst auf Klick und gibt den Leser beim Schließen
  wieder frei. Die App erlaubt höchstens 64 gleichzeitige Leser für alle
  Ansichten zusammen, deshalb liest die Markierung neben dem Zeitstempel nie
  selbst.
