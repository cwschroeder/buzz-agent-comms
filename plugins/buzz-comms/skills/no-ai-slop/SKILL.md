---
name: no-ai-slop
description: Schreibt und redigiert lesergerichtete Texte in der passenden Stimme oder benennt KI-Floskeln, ohne den Text ungefragt umzuschreiben. Vor jeder Buzz-Lifecycle-Nachricht sowie bei Textentwürfen, Überarbeitungen und Stilprüfungen verwenden.
---

# Keine KI-Floskeln

Du schreibst und redigierst wie ein aufmerksamer Mensch. Erhalte Aussage und Stimme des Verfassers, während du den Text klarer und lebendiger machst. Entferne typische KI-Muster, ohne einen eigenständigen Text in glatte Standardprosa zu verwandeln.

## Drei Aufgaben

**Erstellen.** Der Nutzer braucht einen neuen lesergerichteten Text, etwa eine Nachricht, einen Beitrag, ein Memo oder ein Projektupdate. Schreibe im passenden Stimmprofil und prüfe den Entwurf anschließend mit denselben Regeln wie eine Überarbeitung. Gib nur den veröffentlichungsreifen Text zurück, sofern der Nutzer keine Erläuterung verlangt.

**Redigieren.** Der Nutzer liefert einen Entwurf. Nimm nur die wirksamen Änderungen vor, die der Text wirklich braucht. Ergänze einen kurzen Abschnitt `Was geändert wurde` nur dann, wenn der Nutzer eine Überarbeitung oder Erklärung verlangt, nicht bei Texten, die direkt veröffentlicht werden sollen.

**Prüfen.** Der Nutzer fragt, ob ein Text nach KI klingt, oder verlangt ein Audit ohne Überarbeitung. Benenne jedes gefundene Muster aus diesem Skill, zitiere die betroffene Stelle und beschreibe die Korrektur in wenigen Worten. Schreibe den Text nicht um, vergib keine Punktzahl und behaupte nicht, eine KI habe ihn verfasst. KI-Detektoren raten. Benannte Muster liefern überprüfbare Belege. Biete anschließend eine Überarbeitung an.

## Sprache

- Antworte in der Sprache des Entwurfs, der Zielgruppe oder der ausdrücklichen Nutzeranweisung.
- Bei deutschen Eingaben und deutschsprachigem Projektkontext ist Deutsch der Standard. Prüfe den Text dann gegen die deutschen Wörter, Wendungen und Beispiele in diesem Skill und in `eval.md`.
- Bei englischen Ausgaben gelten zusätzlich die erhaltenen englischen Prüfmuster. Übersetze technische Bezeichner, Pfade, Befehle, Zitate und Eigennamen nicht.
- Verwende in deutschen Texten echte Umlaute und `ß`. ASCII-Umschreibungen sind nur in technischen Bezeichnern, Pfaden, Befehlen, URLs oder wörtlich zitiertem Quelltext zulässig.

## Stimmprofil

Lies vor dem Erstellen oder Redigieren einer Buzz-Lifecycle-Nachricht `voice-profile.md` in diesem Skill-Verzeichnis und wende es an. Es ist ein öffentliches, auf diesen Zweck begrenztes Profil. Die aktuelle Nutzeranweisung und belegte Projektfakten haben Vorrang.

Das Profil gilt nur für Buzz-Lifecycle-Kommunikation. Bei anderen Formaten erhältst du die im Entwurf erkennbare Stimme. Leite für dieses Plugin kein privates persönliches Profil ab und füge keines ein.

## Wann nachfragen

Bitte bei einer Überarbeitung oder Prüfung nur dann um den Entwurf, wenn er weder im Gespräch noch in einer Datei oder im relevanten Thread vorliegt. Nutze beim Erstellen den vorhandenen Aufgabenkontext, statt routinemäßig nach einem Entwurf zu fragen.

Wenn Zielgruppe oder Format wirklich unklar sind und das Ergebnis dadurch wesentlich anders ausfallen würde, stelle genau eine Frage: Für wen ist der Text und wo wird er veröffentlicht?

Wenn das Ziel unklar ist, frage, was der Leser nach dem Text denken, fühlen oder tun soll.

## Grundsätze beim Redigieren

- **Erhalte die echte Stimme.** Achte zuerst auf Wortwahl, Rhythmus, Direktheit, Humor, Unsicherheit, Abschweifungen und den Grad der Ausarbeitung. Bewahre die persönlichen Merkmale. Glätte nicht jeden Absatz und schreibe eigenständige Sätze nicht nur für mehr Einheitlichkeit um.
- **Ändere so wenig wie nötig.** Behebe KI-Muster, Fehler, Wiederholungen und unklare Stellen. Lass starke menschliche Sätze stehen. Ein roher Entwurf mit echter Stimme soll danach noch immer nach demselben Menschen klingen.
- **Beginne mit dem Punkt, wenn der Einstieg nichts beiträgt.** Streiche allgemeines Anlaufen. Erhalte persönliche Nebenbemerkungen, Geschichten oder Eingeständnisse, wenn sie Kontext, Spannung oder Charakter schaffen.
- **Ziehe Aussagen nur dann nach vorn, wenn es die Klarheit verbessert.** Zwinge nicht jeden Abschnitt in dasselbe Schema aus Aussage, Detail und Hintergrund.
- **Erhalte die Bedeutung.** Erfinde keine Behauptungen, Beispiele, Zahlen, Zitate oder Meinungen. Frage nach, wenn etwas Wesentliches unklar ist.
- **Mache den Text zugänglich, ohne ihn zu verdummen.** Erhalte Substanz, Nuancen und Präzision. Entferne Fachjargon, überlange Sätze, unnötige Substantivierungen und verwickelte Strukturen nur dort, wo sie das Lesen erschweren.
- **Schreibe aktiv.** `Das Team lieferte am Dienstag` ist klarer als `Die Auslieferung erfolgte am Dienstag`. Gib menschlichen Handlungen nach Möglichkeit ein menschliches Subjekt.
- **Jeder Satz braucht einen Zweck.** Streiche leere Einschränkungen und Einleitungen. Erhalte Wendungen wie `ich denke`, `vielleicht` oder `ehrlich gesagt`, wenn sie echte Unsicherheit, Selbstreflexion oder den gesprochenen Rhythmus ausdrücken.
- **Entwirre Sätze, ohne den Rhythmus zu glätten.** Teile schwer verständliche Sätze und Absätze. Erhalte längere gesprochene Sätze, Fragmente und Tempowechsel, wenn sie klar und charakteristisch sind.
- **Sei konkret.** Namen, Zahlen, Daten, Mechanismen und Beispiele sind stärker als Abstraktionen. Aus `Die Integration verbessert die Effizienz` wird nur dann `Die Integration verkürzt das Deployment von 40 auf 4 Minuten`, wenn diese Messung belegt ist.
- **Schütze konkrete Fakten.** Glätte ein nützliches Detail nicht zu allgemeiner Bedeutung. `Die Review-Zeit sank von 30 auf 8 Minuten` ist stärker als `Das Werkzeug verbessert die Produktivität erheblich`.
- **Lass Verben arbeiten.** `eine Entscheidung treffen` wird `entscheiden`, `hat die Möglichkeit` wird `kann`.
- **Kenne den Zweck.** Kläre vor Struktur und Wortwahl, was der Text erreichen soll und für wen er bestimmt ist.
- **Erhalte Kante und Charakter.** Bewahre deutliche Meinungen, direkte Sprache, Humor, Kraftausdrücke, Selbstunterbrechungen und ehrliche Eingeständnisse, wenn sie zum Verfasser gehören. Ersetze sie nicht durch vermeintlich professionellere Formulierungen.
- **Erhalte die Struktur, solange sie trägt.** Lass die gedankliche Reihenfolge und charakteristische Umwege stehen. Wenn du umstellst, erkläre den Grund im Abschnitt `Was geändert wurde`.

## Wörter und Wendungen zum Streichen

In deutschen Texten meist streichen: `ganzheitlich`, `zukunftsweisend`, `wegweisend`, `bahnbrechend`, `transformativ`, `leistungsstark`, `robust`, `nahtlos`, `effizient gestalten`, `Potenziale heben`, `Mehrwert schaffen`, `auf die nächste Stufe heben`, `ein echter Gamechanger`, `dies verändert alles`.

In englischen Texten streichen: `delve`, `foster`, `leverage`, `utilize`, `facilitate`, `empower`, `streamline`, `robust`, `cutting-edge`, `paradigm shift`, `game changer`, `this is huge`, `this changes everything`, `tapestry`, `realm`, `beacon`, `multifaceted`, `meticulous`, `intricate`, `paramount`, `transformative`, `elevate`, `embark`, `supercharge`, `harness`, `ever-evolving`.

Oft leer sind: `eigentlich`, `wirklich`, `grundsätzlich`, `letztlich`, `einfach`, `natürlich`, `zweifellos`, `selbstverständlich`, `ehrlich gesagt`, `tatsächlich` sowie im Englischen `just`, `literally`, `honestly`, `simply`, `actually`, `truly`, `fundamentally`, `importantly`, `crucially`, `inherently`, `inevitably`. Streiche sie, wenn sie nichts tragen. Erhalte sie, wenn sie echte Betonung, Unsicherheit, Kontrast oder den natürlichen Sprachrhythmus ausdrücken.

Oft leere Einleitungen sind: `Es ist wichtig zu betonen`, `Es ist erwähnenswert`, `An dieser Stelle sei gesagt`, `Wenn es um ... geht`, `In der heutigen Zeit`, `In diesem Zusammenhang`, `Im Grunde genommen`, `Letztendlich`, `Hier ist eine Übersicht`, `Lassen Sie uns eintauchen` sowie die entsprechenden englischen Wendungen `it's worth noting`, `it's important to note`, `at the end of the day`, `when it comes to`, `at its core`, `in today's world`, `in terms of`, `going forward`, `let's dive in`. Streiche sie, wenn sie den Punkt verzögern.

## Muster zum Streichen

**Künstliche Gegensätze.** `Es geht nicht um X. Es geht um Y.` oder `Nicht nur X, sondern auch Y.` Sage Y direkt. Aus `Es geht nicht um das Modell, sondern um die Evaluation` wird `Die Evaluation ist wichtiger als das Modell`.

**Anlaufende Einleitungen.** Streiche `Die Sache ist die`, `Was ich damit sagen will`, `Um es klar zu sagen`, `Ich bin ehrlich` oder `Die unbequeme Wahrheit ist` und beginne mit der Aussage.

**Scheinbare Insider-Erkenntnisse.** Streiche `Was die meisten übersehen`, `Was kaum jemand versteht`, `Der Teil, den alle auslassen` oder `Hier ist, was Ihnen niemand sagt`. Die Behauptung muss ohne Schmeichelei an den Verfasser tragen.

**Dramatische Doppelpunkt-Enthüllungen.** Aus `Das Beste: Das System lernt` wird ein schlichter Satz wie `Das System lernt aus den Korrekturen`. Doppelpunkte sind für Listen, Bezeichnungen und Zitate da, nicht für künstliche Spannung.

**Oberflächliche Deutung.** Streiche angehängte Sätze mit `wodurch die Bedeutung unterstrichen wird`, `was das Engagement verdeutlicht` oder englischen `-ing`-Formen wie `highlighting`, `underscoring`, `reflecting`, `showcasing`. Nenne stattdessen eine konkrete Folge.

**Bedeutungsaufblähung.** `markiert einen wichtigen Meilenstein`, `spielt eine entscheidende Rolle`, `unterstreicht die Bedeutung`, `steht als Beleg für` oder `zeigt eindrucksvoll` ersetzen Fakten durch Wertung. Nenne den Fakt und lass den Leser urteilen.

**Unklare Zuschreibung.** `Experten sind sich einig`, `Studien zeigen`, `Branchenberichte deuten darauf hin`, `viele argumentieren` braucht eine benannte Quelle. Nenne sie oder streiche die Behauptung. Erfinde keine Quelle.

**Künstlich starke Verben.** Verwende `ist` und `hat`, wenn sie klarer sind. Aus `Die Anwendung fungiert als zentrale Plattform für das Sponsorenmanagement` wird `Die Anwendung verwaltet Sponsoren, Entwürfe, Fristen und Freigaben an einem Ort`.

**Synonymwechsel.** Wiederhole das klare Wort, statt für Stil ständig zwischen `Agent`, `Assistent`, `Werkzeug` und `System` zu wechseln.

**Negative Aufzählung.** `Kein X. Kein Y. Ein Z.` wird direkt zu Z.

**Dramatische Fragmente.** Vermeide `X. Und Y. Und Z.` oder `Das ist alles. Mehr braucht es nicht.` Verwende vollständige Sätze, sofern das Fragment nicht erkennbar zur Stimme gehört.

**Roboter-Rhythmus.** Vermeide wiederholte Satzformen, identische Absatzstrukturen und gestapelte kurze Sätze. Verändere den Rhythmus nur, wenn es dem Inhalt hilft.

**Rhetorische Inszenierung.** Streiche `Was wäre, wenn ich Ihnen sage`, `Denken Sie darüber nach`, `Plot Twist` und selbst beantwortete Frage-Antwort-Paare.

**Scheinbar tiefgründiger Schlusssatz.** Lösche die abschließende Metapher, Lebensweisheit oder Pointe, wenn sie nur Tiefe simuliert. Erfinde keine bessere Metapher. Ende mit dem klarsten konkreten Satz, der Aussage oder der nächsten Handlung.

**Zusammenfassender Schluss.** Streiche `Zusammenfassend`, `Abschließend`, `Insgesamt lässt sich sagen`, `Letztendlich` oder einen Schlussabsatz, der den Text nur wiederholt. Ende mit dem letzten konkreten Punkt oder nächsten Schritt.

**Formatierungsfloskeln.** Vermeide Emojis in Überschriften, dekoratives Fettdrucken mitten im Satz, Listen für zwei zusammenhängende Sätze und Überschriften über winzigen Abschnitten. Die Formatierung folgt dem Inhalt.

**Gedankenstriche als Rhythmusstütze.** Verwende in diesem Plugin weder Halbgeviertstriche noch Geviertstriche. Nutze Kommas, Punkte, Klammern oder einen normalen Bindestrich.

## Deutsche Buzz-Texte

- Schreibe echte Umlaute und `ß`. Veröffentliche keine Formen wie `fuer`, `fuenf`, `Naechster`, `Buendel`, `aendern` oder `pruefen` in normaler deutscher Prosa. Erhalte sie nur in Code, technischen Bezeichnern, Pfaden, Befehlen, URLs oder zitiertem Quelltext.
- Streiche übersetzte KI-Einstiege und Rückblicke wie `Hier ist eine Übersicht`, `Es ist wichtig zu betonen`, `Zusammenfassend`, `Abschließend`, `Insgesamt lässt sich sagen` und `nicht nur X, sondern auch Y`. Beginne mit der belegten Wirkung für den Leser oder dem Blocker; der Lieferstatus bleibt im ersten Absatz sichtbar. Erhalte hilfreiche Listen, Tabellen und Vorher/Nachher-Vergleiche.
- Vermeide aufgeblähte Projektsprache wie `wichtiger Meilenstein`, `ganzheitlicher Ansatz`, `zukunftsweisend`, `unterstreicht die Bedeutung` und `zeigt eindrucksvoll`, sofern kein wörtliches Zitat sie verlangt.
- Halte Lifecycle-Nachrichten kompakt. Verwandle einen Commit oder Planstand nicht in einen Mini-Bericht mit dekorativen Überschriften, symmetrischen Abschnitten oder einer Wiederholung am Ende.

## Ablauf

1. Bestimme die Aufgabe: erstellen, redigieren oder prüfen. Kläre Format, Zielgruppe und Sprache.
2. Lies für Buzz-Lifecycle-Texte `voice-profile.md`. Ermittle beim Redigieren außerdem die Kernaussage und drei bis fünf Merkmale der Stimme, die erhalten bleiben müssen. Halte diese Notiz intern. Frage nach, wenn du die Kernaussage nicht erkennen kannst.
3. Gib bei einer reinen Prüfung den unter `Drei Aufgaben` beschriebenen Befund zurück und beende die Arbeit ohne Überarbeitung.
4. Erstelle oder redigiere den Text und prüfe das Ergebnis anschließend selbst vollständig gegen `eval.md`.
5. Behebe jeden fehlgeschlagenen Prüfpunkt und wiederhole die Prüfung.
6. Gib den vollständigen, veröffentlichungsreifen Text zurück. Füge `Was geändert wurde` nur bei einer ausdrücklich verlangten Überarbeitung oder Erklärung hinzu.
