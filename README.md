# **P.A.C.E.r**

**P**räzise **A**bstands-**C**alculierung für ein **E**rfolgreiches Ma**r**athon

## Entwicklung

### Erste Installation

Um **P.A.C.E.r** für die Weiterentwicklung zu installieren, folgen Sie diesen Schritten:

1. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:
    
    Unter Linux:
    ```bash
    python3 -m venv .tm
    source .tm/bin/activate
    ```
    
    Unter Windows:
    ```powershell
    python -m venv .tm
    .tm\Scripts\Activate.ps1
    ```
   

2. Installieren Sie die erforderlichen Pakete:

   ```bash
   pip install -r requirements.txt
   ```
   
### Starten des Entwicklung-Servers

Unter Linux:
   ```bash
   npx tailwindcss -i TurnierManager/static/css/theme.css -o TurnierManager/static/build/theme.css --watch
   python ./TurnierManager/app.py
   ```
   
Unter Windows (in PowerShell):
   ```powershell
   npx tailwindcss -i TurnierManager/static/css/theme.css -o TurnierManager/static/build/theme.css --watch
   python .\TurnierManager\app.py
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