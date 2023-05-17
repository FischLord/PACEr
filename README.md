# **P.A.C.E.r**

**P**räzise **A**bstands-**C**alculierung für ein **E**rfolgreiches Ma**r**athon

## Entwicklung

### Erste Installation

Um **P.A.C.E.r** für die Weiterentwicklung zu installieren, folgen Sie diesen Schritten:

1. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:

   ```bash
   python -m venv .PACEr
   .PACEr/Scripts/Activate.ps1
   ```

2. Installieren Sie die erforderlichen Pakete:

   ```bash
   pip install -r requirements.txt
   ```
   
### Starten des Entwicklung-Servers

   ```bash
   npx tailwindcss -i PACEr/static/css/theme.css -o PACEr/static/build/theme.css --watch
   python .\PACEr\app.py
   ```
    
### Akzentfarben

- Hintergrundfarbe: Grau (`bg-gray-900`)
- Hintergrnud Header/Footer: Grau (`bg-gray-900`)
- Akzentfarbe / Logo: Orange (`text-orange-600`)
- Textfarbe: Hellgrau (`text-gray-400`)
- Hover / Interaktionsfarbe: Orange (`hover:text-orange-600`)
- Randfarbe für interaktive Elemente: Orange (`border-orange-600`)
- Sekundäre Akzentfarbe: Blau (`text-blue-600`)
- Fehlermeldung oder kritische Informationen: Rot (`text-red-600`)
- Erfolgsmeldung oder positive Informationen: Grün (`text-green-600`)
- Warnhinweise: Gelb (`text-yellow-600`)
