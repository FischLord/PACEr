# **P.A.C.E.r**

## **P**räzise **A**bstands-**C**alculierung für ein **E**rfolgreiches Ma**r**rathon


## Development

    ### First Install

    1. Create Virtualenv and Enter it
        '''
        python -m venv .PACEr
        .PACEr/Scripts/Activate.ps1
        '''

    2. Instal Requirements
        '''
        pip install -r .\requirements.txt
        '''

    ### Starting Development Server
    1. Launch CSS Watcher 
    '''
    npx tailwindcss -i PACEr/static/css/theme.css -o PACEr/static/build/theme.css --watch
    '''

    2. Start Flask App
    '''
    python 