# TurnierManager - Redesign Plan

> Umbenennung von PACEr → **TurnierManager**
> PACEr wird zur Kernfunktion innerhalb der App

---

## 🎯 Vision

Eine moderne Webanwendung für Fahrsport-Enthusiasten, die:
- Pace-Berechnungen durchführt (PACEr-Modul)
- Einen öffentlichen Verlauf aller Berechnungen bietet
- Turnierinformationen verwaltet
- OCR für Turnierdokumente unterstützt
- Einfach und benutzerfreundlich ist

---

## 📋 Phase 1: Grundlagen & Architektur

### 1.1 Projekt-Umbenennung & Struktur
- [ ] Umbenennung: PACEr → TurnierManager
- [ ] Neue modulare Projektstruktur:
  ```
  TurnierManager/
  ├── app/
  │   ├── __init__.py          # App Factory
  │   ├── config.py            # Konfiguration (Environment Variables)
  │   ├── extensions.py        # Flask Extensions (DB, Login, etc.)
  │   ├── models/              # Datenbank-Modelle
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   ├── calculation.py
  │   │   ├── tournament.py
  │   │   └── report.py
  │   ├── modules/
  │   │   ├── pacer/           # PACEr als Modul
  │   │   │   ├── __init__.py
  │   │   │   ├── routes.py
  │   │   │   ├── services.py
  │   │   │   └── templates/
  │   │   ├── history/         # Öffentlicher Verlauf
  │   │   ├── ocr/             # OCR-Modul
  │   │   ├── admin/           # Admin-Panel
  │   │   └── auth/            # Authentifizierung
  │   ├── static/
  │   │   ├── css/
  │   │   ├── js/
  │   │   └── img/
  │   └── templates/
  │       ├── base.html
  │       ├── components/      # Wiederverwendbare Komponenten
  │       └── pages/
  ├── migrations/              # Datenbank-Migrationen
  ├── tests/
  ├── .env.example
  ├── requirements.txt
  └── run.py
  ```

### 1.2 Technologie-Stack (Modernisierung)
- **Backend:** Flask 3.x mit Blueprints
- **Datenbank:** SQLite (dev) / PostgreSQL (prod) mit SQLAlchemy
- **Migrations:** Flask-Migrate (Alembic)
- **Auth:** Flask-Login + Werkzeug Security
- **Frontend:** Tailwind CSS 3.x + Alpine.js (leichtgewichtig, reaktiv)
- **OCR:** Tesseract.js (clientseitig) oder pytesseract (serverseitig)
- **Forms:** Flask-WTF mit CSRF-Schutz

### 1.3 Sicherheit
- [ ] Environment Variables für Secrets (.env)
- [ ] Sichere Passwort-Hashing (werkzeug.security)
- [ ] CSRF-Schutz auf allen Formularen
- [ ] Rate Limiting für API-Endpoints
- [ ] Input Validation & Sanitization

---

## 📋 Phase 2: Datenbank & Modelle

### 2.1 Datenbank-Schema

```
┌─────────────────┐     ┌─────────────────────┐
│     User        │     │    Tournament       │
├─────────────────┤     ├─────────────────────┤
│ id (PK)         │     │ id (PK)             │
│ username        │     │ name                │
│ email           │     │ location            │
│ password_hash   │     │ date                │
│ is_admin        │     │ created_at          │
│ created_at      │     └─────────────────────┘
└─────────────────┘              │
                                 │
┌─────────────────────────────────────────────┐
│              Calculation                     │
├─────────────────────────────────────────────┤
│ id (PK)                                      │
│ user_id (FK, nullable) - für anonyme Nutzung │
│ tournament_id (FK, nullable)                 │
│ ─────────────────────────────────────────── │
│ distance_meters                              │
│ speed_kmh                                    │
│ track_type (wegstrecke/hindernis/schritt)   │
│ ─────────────────────────────────────────── │
│ bz_minutes, bz_seconds                       │
│ ez_minutes, ez_seconds                       │
│ hz_minutes, hz_seconds                       │
│ ─────────────────────────────────────────── │
│ class_name (Klasse: z.B. "M", "S")          │
│ test_name (Prüfung: z.B. "Marathon A")      │
│ notes (optional)                             │
│ is_public (Boolean)                          │
│ ─────────────────────────────────────────── │
│ created_at                                   │
│ ip_hash (für Spam-Schutz, anonymisiert)     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│              Report (Bug Reports)            │
├─────────────────────────────────────────────┤
│ id (PK)                                      │
│ user_id (FK, nullable)                       │
│ name, email                                  │
│ issue_type                                   │
│ description                                  │
│ status (open/in_progress/resolved)          │
│ admin_notes                                  │
│ created_at                                   │
└─────────────────────────────────────────────┘
```

---

## 📋 Phase 3: Features

### 3.1 PACEr-Modul (Kernfunktion)
- [ ] Bestehende Rechner-Logik übernehmen
- [ ] Alten Rechner entfernen (nur eine Version)
- [ ] Verbesserte Ergebnis-Darstellung:
  - Übersichtliche Tabelle
  - Grafische Pace-Visualisierung (Chart.js)
  - Export als PDF
  - Export als CSV
- [ ] "Zum Verlauf hinzufügen" Option nach Berechnung

### 3.2 Öffentlicher Verlauf (NEU)
- [ ] Liste aller öffentlichen Berechnungen
- [ ] Filter nach:
  - Turnier
  - Datum
  - Klasse/Prüfung
  - Streckenart
- [ ] Suche nach Turniernamen
- [ ] Sortierung (neueste zuerst, nach Turnier, etc.)
- [ ] Pagination für Performance
- [ ] "Schnellzugriff" - beliebte/aktuelle Turniere oben

**Ablauf für Nutzer:**
1. Berechnung durchführen
2. Optional: "Öffentlich teilen" aktivieren
3. Turnier/Klasse/Prüfung auswählen oder eingeben
4. Berechnung erscheint im öffentlichen Verlauf

### 3.3 Turnier-Verwaltung (NEU)
- [ ] Turniere können von Admins angelegt werden
- [ ] Nutzer können beim Teilen ein Turnier auswählen
- [ ] Oder neues Turnier vorschlagen (Admin-Freigabe)
- [ ] Turnier-Detailseite mit allen zugehörigen Berechnungen

### 3.4 OCR-Funktion (NEU)
- [ ] Bild/PDF hochladen
- [ ] Automatische Erkennung von:
  - Streckenlänge
  - Zeitvorgaben
  - Turniername (wenn vorhanden)
- [ ] Vorausfüllung des Rechners mit erkannten Werten
- [ ] Nutzer kann Werte korrigieren vor Berechnung

**Technische Optionen:**
- **Option A:** Tesseract.js (clientseitig, kein Server-Upload nötig)
- **Option B:** pytesseract (serverseitig, mehr Kontrolle)
- **Empfehlung:** Tesseract.js für Datenschutz + Performance

### 3.5 Admin-Panel (Überarbeitung)
- [ ] Sicheres Login (gehashte Passwörter)
- [ ] Dashboard mit Statistiken:
  - Berechnungen pro Tag/Woche/Monat
  - Beliebte Turniere
  - Aktive Nutzer
- [ ] Berechnungs-Verwaltung:
  - Öffentliche Einträge ansehen
  - Spam/Fehlerhafte Einträge löschen
  - Einträge bearbeiten
- [ ] Turnier-Verwaltung:
  - Turniere anlegen/bearbeiten/löschen
  - Vorgeschlagene Turniere freigeben
- [ ] Bug-Reports:
  - Status ändern (offen → in Bearbeitung → gelöst)
  - Notizen hinzufügen
- [ ] Benutzer-Verwaltung (optional):
  - Nutzer sperren bei Missbrauch

### 3.6 Weitere Feature-Ideen
- [ ] **Favoriten:** Häufig verwendete Einstellungen speichern
- [ ] **Vergleich:** Zwei Berechnungen nebeneinander vergleichen
- [ ] **Benachrichtigungen:** Email bei neuem Turnier-Eintrag
- [ ] **API:** REST-API für externe Integrationen
- [ ] **PWA:** Als App installierbar (offline-fähig für Grundfunktionen)
- [ ] **Mehrsprachigkeit:** DE/EN Support
- [ ] **Dark/Light Mode:** Theme-Umschaltung

---

## 📋 Phase 4: UI/UX Redesign

### 4.1 Design-Prinzipien
- **Klarheit:** Weniger ist mehr, fokussierte Oberfläche
- **Mobile First:** Primär für Smartphone-Nutzung optimiert
- **Schnelligkeit:** Hauptfunktion (Rechner) sofort erreichbar
- **Konsistenz:** Einheitliches Design-System

### 4.2 Farbschema (Vorschlag)
```
Primary:     #2563EB (Blau) - Vertrauenswürdig, professionell
Secondary:   #10B981 (Grün) - Erfolg, positive Aktionen
Accent:      #F59E0B (Orange/Amber) - Call-to-Actions
Background:  #F9FAFB (Hell) / #111827 (Dunkel)
Text:        #1F2937 (Dunkel) / #F9FAFB (Hell)
Error:       #EF4444 (Rot)
```

### 4.3 Seitenstruktur

```
┌─────────────────────────────────────────────┐
│  🏠 TurnierManager                    [≡]   │  ← Header/Nav
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      🧮 PACEr - Pace Rechner        │   │  ← Hero/Quick Access
│  │      [Jetzt berechnen]              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📋 Aktuelle Berechnungen                  │  ← Öffentlicher Verlauf
│  ┌─────────────────────────────────────┐   │
│  │ Turnier XY | M-Klasse | 3200m      │   │
│  │ BZ: 4:20 | EZ: 6:40 | HZ: 8:00     │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │ Turnier AB | S-Klasse | 2800m      │   │
│  └─────────────────────────────────────┘   │
│  [Mehr anzeigen...]                        │
│                                             │
├─────────────────────────────────────────────┤
│  🏠 Home | 🧮 Rechner | 📋 Verlauf | ℹ️ Info │  ← Bottom Nav (Mobile)
└─────────────────────────────────────────────┘
```

### 4.4 Komponenten
- [ ] Modernes Card-Design für Berechnungen
- [ ] Floating Action Button für schnelle Berechnung
- [ ] Toast-Benachrichtigungen statt Modals
- [ ] Skeleton Loading States
- [ ] Responsive Tabellen
- [ ] Interaktive Charts für Ergebnisse

---

## 📋 Phase 5: Code-Cleanup

### 5.1 Zu entfernen
- [ ] `pacerOld.html` und `pacerOld.js` (alter Rechner)
- [ ] `pacerSwitch.js` (nicht mehr nötig)
- [ ] Hardcoded Passwörter
- [ ] Alte JSON-basierte Report-Speicherung
- [ ] Redundante CSS-Klassen

### 5.2 Zu refactoren
- [ ] `helper.py` → aufteilen in Services
- [ ] Route-Handler → schlanker, Logik in Services
- [ ] Templates → Komponenten-basiert
- [ ] JavaScript → Modular mit ES6 Imports

---

## 📋 Phase 6: Implementierungs-Reihenfolge

### Sprint 1: Foundation
1. Neue Projektstruktur aufsetzen
2. Datenbank + Modelle implementieren
3. Flask-Migrate einrichten
4. Basis-Templates (Layout, Navigation)
5. Konfiguration über Environment Variables

### Sprint 2: Core Features
1. PACEr-Modul migrieren
2. Neues UI für Rechner
3. Ergebnis-Seite mit Charts
4. PDF/CSV Export

### Sprint 3: Verlauf & Turniere
1. Öffentlicher Verlauf implementieren
2. Filter & Suche
3. Turnier-Modell & Verwaltung
4. "Teilen"-Funktion bei Berechnungen

### Sprint 4: OCR & Admin
1. OCR-Integration (Tesseract.js)
2. Admin-Panel Redesign
3. Statistik-Dashboard
4. Bug-Report Überarbeitung

### Sprint 5: Polish & Launch
1. UI/UX Feinschliff
2. Performance-Optimierung
3. Testing
4. Dokumentation
5. Deployment-Setup

---

## ❓ Offene Fragen

1. **Benutzerkonten:** Sollen sich Nutzer registrieren können, oder reicht anonyme Nutzung mit optionalem Admin-Account?

2. **OCR-Umfang:** Welche Art von Dokumenten sollen erkannt werden? (Ausschreibungen, Startlisten, Ergebnislisten?)

3. **Hosting:** Wo soll die App gehostet werden? (PythonAnywhere, Heroku, eigener Server?)

4. **Priorität:** Welches Feature ist am wichtigsten für den ersten Release?

---

## 📝 Notizen

- Bestehende Berechnungslogik ist solide → übernehmen
- Stats.json Daten können initial migriert werden
- Alte Reports können optional importiert werden

---

*Plan erstellt: 2026-01-10*
*Version: 1.0*
