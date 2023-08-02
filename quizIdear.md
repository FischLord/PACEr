Hier ist die überarbeitete Projektübersicht in einer Markdown-formatierten Ansicht, zusammen mit den beiden JSON-Musterdateien, die jeweils zwei Beispiel-Fragen enthalten:

# Projektübersicht - Quiz-Web-App mit Flask

## Beschreibung
- Ziel: Erstellen einer Quiz-Web-App mit Flask.
- Die Web-App wird eine Quiz-App sein, die dem Nutzer Fragen stellt und ihm erlaubt, Antworten auszuwählen.
- Es wird eine Admin-Oberfläche geben, um Fragen im JSON-Format zu verwalten (hinzufügen, bearbeiten, löschen).
- Die Fragen werden in einem JSON-Format gespeichert.

## Funktionalitäten

### Admin-Oberfläche
- Anlegen eines HTML-Formulars zur Eingabe von Fragen:
  - Kategorie: Eine vorgefertigte Liste von Kategorien.
  - Fragestellung: Freitext für die Frage.
  - Antwortmöglichkeiten: Liste von Antwortmöglichkeiten, aus denen der Nutzer auswählen kann.
  - Mehrere richtige Antworten: Möglichkeit, mehrere richtige Antworten zu markieren.
  - Bild: Möglichkeit, Bilder als Teil der Frage hinzuzufügen (z. B. Beschriftung oder Informationsquelle).
  - Schwierigkeitsstufe: Eine Bewertung der Schwierigkeitsstufe auf einer Skala von 1 bis 10.
  - Optionales Feld für eine kleine Erklärung zur Lösung.

### Datenverwaltung
- Die eingegebenen Fragen werden in einem JSON-Dateiformat gespeichert.
- Automatische Vergabe einer eindeutigen Frage-ID mit jeder neu hinzugefügten Frage.
- Die Admin-Oberfläche ermöglicht das Bearbeiten und Löschen vorhandener Fragen.

### Statistiken
- Die Statistiken werden in einer separaten JSON-Datei gespeichert, um sie unabhängig von den Fragen zu verwalten.

## Technologien
- Flask: Verwendung des Flask-Frameworks für die Web-App.
- HTML: Erstellen des HTML-Formulars für die Admin-Oberfläche.
- JSON: Speichern der Fragen in einem JSON-Dateiformat, inklusive der Statistiken in einer separaten JSON-Datei.

## Beispiel-Musterdatei - questions.json

```json
{
  "questions": [
    {
      "id": 1,
      "category": "Geschichte",
      "question": "Wann wurde die Berliner Mauer erbaut?",
      "difficulty": 4,
      "explanation": "Die Berliner Mauer wurde im Jahr 1961 errichtet.",
      "image": "berlin_wall.jpg",
      "answers": [
        "1955",
        "1961",
        "1989",
        "1995"
      ],
      "correct_answers": [1]
    },
    {
      "id": 2,
      "category": "Informatik",
      "question": "Was steht für HTML?",
      "difficulty": 2,
      "explanation": "HTML steht für Hypertext Markup Language.",
      "answers": [
        "Hyper Text Markup Language",
        "High Tech Machine Learning",
        "Home Tool Management Language",
        "Hyperlinks and Text Markup Language"
      ],
      "correct_answers": [0]
    }
  ]
}
```

## Beispiel-Musterdatei - statistics.json

```json
{
  "statistics": {
    "1": {
      "total_attempts": 15,
      "correct_attempts": 12
    },
    "2": {
      "total_attempts": 20,
      "correct_attempts": 16
    }
  }
}
```

In den Beispiel-Musterdateien "questions.json" und "statistics.json" sind jeweils zwei Fragen enthalten. Die erste Frage hat eine einzige richtige Antwort, während die zweite Frage mehrere mögliche Antworten hat.

Bei der Umsetzung Ihres Projekts können Sie die tatsächlichen Fragen hinzufügen und die JSON-Dateien entsprechend erweitern. Viel Erfolg! Falls Sie weitere Unterstützung benötigen, stehe ich Ihnen gerne zur Verfügung.