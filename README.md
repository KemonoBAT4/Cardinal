# Cardinal - Alpha 0.1.2

### What is Cardinal 🔭
The idea of cardinal is to create a program that can help creating a backend structure with a complete dashboard to handle taks, manage possible webistes, bots or handle different datas.
Once its core features are completed, Cardinal will be, with some simple commands, able to completely create new applications in the interface, apply some defaults routes, handle users. Once the application is completed, a single Cardinal project installed will be able to run multiple applications simultaneously without, everything with its own database and configurations, but all on the same core.

## How to install Cardinal 🖥️
### Production Branch Installation
There is currently not a production branch with a stable way to install & run Cardinal, since its still in development.

### Development Branch Installation
In this first version of Cardinal the first way to start as development an application is the following:

- download the application with the command on a terminal `git clone https://github.com/KemonoBAT4/Cardinal`
- enter the folder with `cd Cardinal`
- create a python environment and activate it ( see how you can activate a virtual environment [here](https://github.com/KemonoBAT4/Cardinal/blob/main/core/docs/Environment.md) )
- install all the dependencies with the command `pip install -r requirements.txt`
- now its possible to run Cardinal, for a list of arguments possible run `python run.py help`
- for a list of all the possible applications run the command `python run.py list`
- for a simple setup of an application, before running it, do `python run.py <application name> setup`
- now its possible to run the command `python run.py <application name> run`

<!--  (- install all the requirements with `pip install -r requirements.txt`) -->
<!--  (- run cardinal with `python run.py`) -->
<!--  (- visit the dashboard page `/cardinal/dashboard` to see the dashboard) -->

## Contribute the project 📋
If you have access to this repository you are free to fork the dev branch to help the project.
When you are done developing pls make a pull request [here](https://github.com/KemonoBAT4/Cardinal/pulls) providing a detailed description of all the changes you made. A complete guide on how to make a standard pull request can be found [here](https://github.com/KemonoBAT4/Cardinal/blob/main/core/docs/Contributing.md).

## Structure 📂
A structure of the project can be found [here](https://github.com/KemonoBAT4/Cardinal/blob/main/core/docs/Structure.md) with some details about the folder's utility.

## Versions 🗄️
Right now, Cardinal's version is `Alpha 0.1.2`, and wil be updated when there is a new important feature added or bugs fixed. More About Versions
[here](https://github.com/KemonoBAT4/Cardinal/blob/main/core/docs/Versions.md).

## Ideas & Suggestions 💡
A complete list of ideas that its currently in development / considered can be found [here](https://github.com/KemonoBAT4/Cardinal/blob/main/core/docs/Ideas.md) and in its related Issues (only for W.I.P. ideas).
