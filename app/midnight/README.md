
# Midnight
Midnight is a desktop & mobile application made to handle basic tasks & projects with a little help of a small AI as support


## 1.  📌 Getting Started
Commands to run the server in dev mode. For more commands, parameters and specific behaviour, see the specific files for more accurate infos.

- Run the project:
    - **`./run.sh <project_name> run`**

- Act on the database:
    - **`./run.sh <project_name> reset`** resets the database
    <!-- - **`./run.sh <project_name> --migrate`** migrates the database without removing the data
    - **`./run.sh <project_name> --shell`** opens the database shell to execute action on the db of the project -->

- Set up basic data (edit the setup function in `cli.py` for every specifi project)
    - **`./run.sh <project_name> setup`**


## 2. 🏗️ Deploy The Project
Follow these steps to make a deploy folder for this project:

1. First run this command to create the compiled folder.
    - **`./run.sh <project_name> build`**

this will create a .tar folder which is the image

2. For running the compiled instance the following command
    - **`docker run cardinal-<project_name> <project_name> <command>`**

