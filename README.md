# Cardinal

### What is the Cardinl System
The idea of cardinal is to create a program that can handle, learn and automate from simple to complex tasks like managing websites, bots or even
for moderation. The ultimate goal is to merge all the different projects and make them work on a single platform, removing all the problems that 
might generate wrong configurations. Once the core is ultimated and perfectly functioning, to create a new application on cardinal will only require to pass the repository link of a project
and selecting the starting file, cardinal then will be able to download the project, install all dependecies and create a personalized command for the user to start the application directly from cardinal.

## Getting Started
### How to run Cardinal

 - install all the requirements with `pip install -r requirements.txt`
 - run cardinal with `python run.py`
 - visit the dashboard page `/cardinal/dashboard` to see the dashboard

## The idea of Cardinal
Right now cardinal can create multiple tables on a single database for all the applications + the core, this will be changed so every application has its own sub-core and configuration, making calls to the main cardinal to send analytics data, informations, statuses and other, also the Users will be set in the main Cardinal and redistribuited through the application, without the need to create an account every time, the project will be executed in a small beta with a discord bot made in node js and a old webiste also made in node js and the api that will be used is the cardinal application

### Contribute the project
If you have access to this repository you are free to fork the dev branch to help the project.
When you are done developing pls make a pull request [here](https://github.com/KemonoBAT4/Cardinal/pulls) providing a detailed description of all the changes you made


```
Cardinal/
├── core/                 # codice riutilizzabile, models, utils
|    ├── cardinal/
|    ├── docs/
|    ├── handlers/
|    ├── models/
|    ├── system/
|    |    ├── __init__.py # espone la classe Cardinal e aggiunge la configurazione con il cfg esterno
|    |    ├── cardinal.py # codice contenente l'applicazione flask, posso condividere il codice
|    ├── web/
├── docker-compose.yml    # generico, parametrico
├── run.py                # entrypoint
├── application.cfg 	   # la configurazione generale per l'applicazione (potrebbe essere inutile)
├── Dockerfile
├── app/
│   ├── example1/         # un'esempio generico di un'applicazione
│   │   ├── application.cfg
│   │   ├── routes.py
│   │   ├── api.py
│   └── example2/
│       ├── application.cfg
│       ├── routes.py
│       ├── api.py
```