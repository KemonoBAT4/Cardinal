
```
Cardinal/                                           - THE MAIN FOLDER
├── app/                                            - THE APPLICATION FOLDER
|    └── .../
|         ├── api.py                                - ONLY API SCRIPT
│         ├── application.cfg                       - APPLICATION CONFIG
│         ├── forms.py                              - THE APPLICATIONS FORMS
│         ├── handlers.py                           - FUNCTIONS
│         ├── menu.json                             - THE LEFT MENU
│         ├── models.py                             - THE MODELS FOR THE DATA
│         └── routes.py                             - MAIN ROUTES
├── core/                                           - THE CORE (not to touch)
|    ├── configs/                                   - THE CARDINAL CONFIGS
|    |    ├── __init__.py
|    |    └── config.py                             - THE ACTUAL CONFIG SCRIPT
|    ├── database/                                  - THE DATABASE FOLDER
|    |    └── database.db                           - THE DATABASE ( W.I.P. )
|    ├── docs/                                      - CARDINAL'S DOCUMENTATION
|    |    ├── documentation/                        - HOW TO USE CARDINAL
|    |    |    ├── Creating a new Application.md
|    |    |    ├── Creating the models.md
|    |    |    ├── Understanding the Commands.md
|    |    |    ├── Using Cardinal.md
|    |    |    └── temp-models.json
|    |    ├── example/                              - AN EXAMPLE FOR SETUP
|    |    |    ├── api.py
|    |    |    ├── application.cfg
|    |    |    ├── forms.py
|    |    |    ├── handlers.py
|    |    |    ├── models.py
|    |    |    └── routes.py
|    |    └── Structure.md                          - THE APP STRUCTURE
|    ├── handlers/                                  - CARDINAL HANDLERS FOLDER
|    |    └── handlers.py                           - THE HANDLERS
|    ├── models/                                    - CARDINAL MODELS FOLDER
|    |    ├── __init__.py
|    |    ├── base.py                               - THE BASE FOR THE APPS
|    |    └── models.py                             - SOME CUSTOM MODELS
|    ├── system/                                    - THE CORE OF CARDINAL
|    |    ├── __init__.py
|    |    └── cardinal.py                           - MAIN APPLICATION CLASS
|    └── web/                                       - THE WEB FOLDER
|         ├── icons/                                - ICONS FOLDER
│         │    ├── favicon.ico
│         │    └── icon.png
|         ├── scripts/                              - THE SCRIPTS FOLDER
│         │    ├── index - old.js
│         │    └── index.js                         - THE PAGE COMPON. SCRIPT
|         ├── styles/                               - THE STYLES FOLDER
│         │    ├── index - old.css
│         │    └── index.css                        - THE PAGE COMPON. CSS
|         ├── templates/                            - ALL THE HTML TEMPLATES
│         │    ├── card.html                        - THE CARD TEMPLATE
│         │    ├── index - old.html
│         │    ├── index.html                       - THE MAIN PAGE TEMPLATE
│         │    └── section.html                     - THE SECTION TEMPLATE
|         ├── __init__.py
|         ├── api.py                                - CARDINAL'S WEB API
|         ├── handlers.py                           - CARDINAL'S WEB HANDLERS
|         ├── menu.py                               - CARDINAL'S WEB MENU
|         ├── pages.py                              - PAGE CREATIONS SCRIPTS
|         ├── routes.py                             - CARDINAL'S WEB ROUTES
|         └── users.py                              - W.I.P.
├── .gitignore
├── application.cfg                                 - CARDINAL DEFAULT CONFIG
├── cardinal.log                                    - SIMPLE LOGGER (W.I.P.)
├── docker-compose.yml
├── dockerfile
├── LICENCE.txt                                     - THE LICENCE
├── README.md                                       - MAIN README
├── requirements.txt
└── run.py                                          - MAIN RUNNER
```