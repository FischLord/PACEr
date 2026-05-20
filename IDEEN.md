# PACEr Ideen & Wünsche

Diese Datei sammelt bewusst lose Ideen für später. Ein Eintrag hier ist keine aktive Aufgabe und hat keine Umsetzungszusage.

## Höhere Priorität

### SEO-Basis ausbauen

- Aktueller Stand: solide Grundlage, aber noch nicht vollständig SEO-fertig.
- Seitenspezifische Titel und Meta-Descriptions für Startseite, Rechner, Turniere, Über mich, Impressum und Feedback ergänzen.
- Canonical URLs setzen.
- Doppelte Startseiten-Inhalte klären: `/` und `/projektInfo` zeigen aktuell denselben Inhalt; entweder Canonical auf `/` oder Redirect einführen.
- `robots.txt` ergänzen.
- `sitemap.xml` ergänzen.
- Admin-/Login-/interne Seiten auf `noindex` setzen oder per `robots.txt` ausschließen.
- Relevante Suchbegriffe organisch in Texte einarbeiten, z. B. Fahrsport Marathon Zeitrechner, Bestzeit, Erlaubte Zeit und Höchstzeit berechnen.

## Mittlere Priorität

### Strukturierte Daten

- JSON-LD für PACEr als WebApplication prüfen.
- Optional strukturierte FAQ-Daten für die Feedback-/FAQ-Seite ergänzen.
- Optional Organization-/Website-Daten ergänzen, sobald Domain und öffentliche URLs final sind.

## Niedrige Priorität

### Mehrsprachigkeit

- Idee: Sprache der öffentlichen Seite umschaltbar machen, z. B. Deutsch/Englisch.
- Denkbarer Einstieg: Deutsch bleibt Standard; zuerst nur öffentliche Seiten und Rechner übersetzen.
- Admin-Bereich kann vorerst Deutsch bleiben.
- Technischer Ansatz für später: eher Flask-Babel als dauerhaftes Übersetzungssystem statt selbst gebauter Dictionaries.
- Offene fachliche Frage: Begriffe wie Bestzeit, Erlaubte Zeit, Höchstzeit, Wegstrecke und Hindernisstrecke sauber übersetzen oder deutsch lassen und erklären.
