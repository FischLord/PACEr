# **P.A.C.E.r**

**P**räzise **A**bstands-**C**alculierung für ein **E**rfolgreiches Ma**r**athon

## Docker und Coolify

Das mehrstufige `Dockerfile` baut CSS mit Node und `npm ci && npm run build:css`
(Tailwind 3). Die npm-Dateien einschließlich Lockdatei sind versioniert; generiertes
`PACEr/static/build/theme.css` bleibt außerhalb des Repos. Die Python-3.12-Laufzeit
enthält Gunicorn, läuft als `pacer` (UID/GID `10001:10001`) und lauscht intern per
HTTP auf Port **8000**. `GET /healthz` liefert ohne Login oder Datenbankabfrage 200;
der Docker-Healthcheck verwendet Python und benötigt kein curl.

### Umgebungsvariablen

Geheimnisse ausschließlich als Laufzeitvariablen hinterlegen, nicht als Build-Argumente.
Für Produktion und Vorschauen getrennte Geheimnisse verwenden.

| Name | Bedeutung | Produktion / Vorschau |
| --- | --- | --- |
| `SECRET_KEY` | Stabiler, zufälliger Schlüssel für Sitzungssignaturen; ohne Vorgabe bei jedem App-Start zufällig. | In beiden setzen; Vorschau getrennt von Produktion. |
| `ADMIN_PASSWORD` | Initialpasswort für `admin`; ohne oder bei leerem Wert wird kein Admin angelegt. Ein vorhandener Admin wird nie geändert. | Zur Ersteinrichtung setzen; in Vorschauen eigenes Passwort oder weglassen. |
| `DATABASE_URL` | Datenbankverbindung; im Image bereits `sqlite:////data/pacer.db`. Außerhalb Docker bleibt der bisherige lokale Fallback erhalten. | Gleicher Containerpfad, aber getrennte Volumes pro Umgebung/PR. |
| `SESSION_COOKIE_SECURE` | Schaltet sichere Sitzungscookies ein (`true`, `1`, `yes`, `on`); Standard aus für lokale HTTP-Entwicklung. | Bei HTTPS in beiden einschalten. |
| `PROXY_FIX_X_FOR` | Anzahl vertrauenswürdiger Werte rechts in `X-Forwarded-For`; Standard 2. | An die tatsächlich angehängten Werte der Proxy-Kette anpassen. |
| `PROXY_FIX_X_PROTO` | Entsprechend für `X-Forwarded-Proto`; Standard 1. | In beiden passend zur Proxy-Konfiguration. |
| `PROXY_FIX_X_HOST` | Entsprechend für `X-Forwarded-Host`; Standard 1. | In beiden passend zur Proxy-Konfiguration. |
| `ASSET_VERSION` | Cache-Version statischer Dateien; Laufzeitwert überschreibt den Image-Wert. Auch als Build-Argument möglich. | Je Build/Deployment, idealerweise Commit-ID; Fallback `local`. |
| `SOURCE_COMMIT` | Optionales Build-Argument als Vorgabe für `ASSET_VERSION`. | In Coolify bei Bedarf für den Build verfügbar machen. |
| `ANTHROPIC_API_KEY` | Optionaler API-Schlüssel für OCR. | Vorschauen ohne Schlüssel oder mit separatem Testschlüssel. |
| `WEB_CONCURRENCY` | Anzahl Gunicorn-Worker; Standard 1. | Standard beibehalten, insbesondere bei SQLite und Ersteinrichtung. |
| `GUNICORN_THREADS` | Threads je Worker; Standard 4. | In beiden bei Bedarf anpassen. |

### Speicher und Proxys

Ein persistentes **Volume auf `/data`** mounten. SQLite einschließlich Journal und
temporäre Dateien (`/data/tmp`) liegen dort; Logs gehen auf stdout/stderr. Ein
neues Docker-Volume übernimmt die Verzeichnisrechte aus dem Image. Bestehende
Volumes und Hostverzeichnisse müssen UID/GID `10001:10001` Schreibzugriff erlauben.
Das Image funktioniert auch mit schreibgeschütztem Container-Dateisystem.

Vorhandene Produktionsdatenbanken bewusst und gesichert ins Produktionsvolume
übernehmen; der Image-Build kopiert keine Datenbank. Vorschauen beginnen mit einem
eigenen leeren Volume und dürfen weder die Produktionsdatenbank noch deren
Hostverzeichnis verwenden. Bei erneutem Deployment desselben PRs darf dessen
eigenes Volume erhalten bleiben. Für einen vollständigen Reset nur dieses löschen.

Nginx Proxy Manager beendet TLS und reicht HTTPS-Schema und öffentlichen Host über
Traefik weiter. Traefik muss die Forwarded-Header des Nginx-Proxy-Managers als
vertrauenswürdig übernehmen (dessen IP/Netz gezielt freigeben). Die Standards
erwarten zwei Einträge für die Client-IP und jeweils einen für Schema/Host. Bei nur
einem IP-Eintrag `PROXY_FIX_X_FOR` auf 1 setzen; ohne Proxy alle drei Zähler auf 0.
Maßgeblich sind die tatsächlich vom Proxy gesetzten Werte je Header, nicht allein
die Anzahl der Prozesse. Den App-Port nur über die vorgesehenen Proxys erreichbar
machen. Details: [Werkzeug ProxyFix](https://werkzeug.palletsprojects.com/en/stable/middleware/proxy_fix/).

### Coolify einrichten

1. GitHub-Quelle `FischLord/PACEr`, Branch `main`, Build-Pack **Dockerfile**,
   Basisverzeichnis `/`, Dockerfile `/Dockerfile`, interner Port `8000`.
   **Auto Deploy / Deploy on push** einschalten; GitHub-App oder Repository-Webhook
   für Push-Ereignisse verbinden.
2. In Coolify `http://pacer.apps.j-rz.de` als Domain eintragen;
   öffentliches HTTPS endet am Nginx Proxy Manager, der Upstream nutzt HTTP.
   In Traefik für diese Route keine zusätzliche HTTPS-Weiterleitung aktivieren.
   Später kann die Domain auf `pacer.j-rz.de` wechseln, ohne Codeänderung.
3. Laufzeitvariablen und Volume für `/data` konfigurieren. Den im Dockerfile
   enthaltenen Healthcheck nutzen (`http://127.0.0.1:8000/healthz`). Für Commit-basierte Asset-Versionen
   `SOURCE_COMMIT` als Build-Argument verfügbar machen oder `ASSET_VERSION` setzen.
4. **Preview Deployments** aktivieren, Pull-Request-Ereignisse der GitHub-App bzw.
   des Webhooks verbinden. Domainvorlage
   `pacer-pr{{pr_id}}.preview.j-rz.de` (erbt intern HTTP) sowie Wildcard-DNS und TLS im
   Nginx Proxy Manager einrichten; öffentlich ist die Vorschau per HTTPS erreichbar.
   Produktions- und Vorschauvariablen getrennt
   pflegen; die `/data`-Volumes müssen je PR unterschiedlich sein. Dafür von
   Coolify verwaltete, pro Vorschau getrennte Volumes verwenden und die tatsächlich
   zugeordneten Volumenamen vor dem ersten Vorschau-Start prüfen.

Die Coolify-Einstellungen werden auf dem Server vorgenommen. Anleitung:
[Dockerfile](https://coolify.io/docs/applications/builds/dockerfile),
[Auto-Deploy](https://coolify.io/docs/applications/deployments/automatic-deployments),
[PR-Vorschauen](https://coolify.io/docs/applications/deployments/preview-deployments),
[Speicher](https://coolify.io/docs/applications/configuration/persistent-storage).

### Lokal mit Docker prüfen

`SECRET_KEY` und `ADMIN_PASSWORD` vorher in der Shell setzen (keine Werte ins Repo).
Für diesen HTTP-Test bleibt `SESSION_COOKIE_SECURE` aus; unter HTTPS einschalten.

```bash
docker build -t pacer:local .
docker volume create pacer-local-data
docker run -d --name pacer-local --read-only -p 127.0.0.1:8000:8000 \
  --mount source=pacer-local-data,target=/data \
  -e SECRET_KEY -e ADMIN_PASSWORD -e SESSION_COOKIE_SECURE=false pacer:local
docker inspect --format '{{.State.Health.Status}}' pacer-local
```

Startseite und CSS, `/healthz`, Admin-Login und Rechner über
`http://localhost:8000` prüfen. Eine Berechnung speichern, deren PDF-URL notieren,
`docker restart pacer-local` ausführen und dieselbe PDF-URL erneut öffnen.
Für einen Austauschtest den Container entfernen und mit demselben Volume neu
anlegen; die Daten bleiben erhalten. Für eine isolierte Vorschau ein anderes,
leeres Volume verwenden.

## Entwicklung

### Erste Installation

Um **P.A.C.E.r** für die Weiterentwicklung zu installieren, folgen Sie diesen Schritten:

1. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:
    
    Unter Linux:
    ```bash
    python3 -m venv .PACEr
    source .PACEr/bin/activate
    ```
    
    Unter Windows:
    ```powershell
    python -m venv .PACEr
    .PACEr\Scripts\Activate.ps1
    ```
   

2. Installieren Sie die erforderlichen Pakete:

   ```bash
   pip install -r requirements.txt
   ```
   
### Tests ausführen

Die vorhandenen Python-Unit-Tests können ohne zusätzliche Test-Abhängigkeit mit `unittest` gestartet werden:

```bash
.PACEr/bin/python -m unittest discover -s tests -v
```

Die JavaScript-Tests für die clientseitige Rechnerlogik laufen direkt über Node:

```bash
node tests/js/pace-core.test.js
```

### Starten des Entwicklung-Servers

Unter Linux:
   ```bash
   npx tailwindcss -i PACEr/static/css/theme.css -o PACEr/static/build/theme.css --watch
   python ./PACEr/app.py
   ```
   
Unter Windows (in PowerShell):
   ```powershell
   npx tailwindcss -i PACEr/static/css/theme.css -o PACEr/static/build/theme.css --watch
   python .\PACEr\app.py
   ```
    
### Akzentfarben
 
- Hintergrundfarbe: Grau (`bg-gray-900`)
- Hintergrnud Header/Footer: Grau (`bg-gray-800`)
- Akzentfarbe / Logo: Orange (`text-orange-600`)
- Textfarbe: Hellgrau (`text-gray-400`)
- Hover / Interaktionsfarbe: Orange (`hover:text-orange-600`)
- Randfarbe für interaktive Elemente: Orange (`border-orange-600`)
- Sekundäre Akzentfarbe: Blau (`text-blue-600`)
- Fehlermeldung oder kritische Informationen: Rot (`text-red-600`)
- Erfolgsmeldung oder positive Informationen: Grün (`text-green-600`)
- Warnhinweise: Gelb (`text-yellow-600`)
