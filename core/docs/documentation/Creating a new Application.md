# Creating a new Application
Here's a small guide on how to create a new application with Cardinal
Currently there are `1` ways to create a new app, here's the list.

## Methods Available:

### Self creation:
This method allows you to create a new application starting from a template and then expanding it on your own, providing a more flexible and customizable experience than all the other methods. The requirements are pretty specific but are required if you want to take out the best of this

- ##### `Requirements:`
    - A good knowledge of Python is required. You should be familiar with concepts such as classes, objects, decorators, and so on

    - A good knowledge of Flask is required. You should be familiar with concepts such as routes, blueprints, templates, and so on

    - A good knowledge of SQLAlchemy queries is required. You should be familiar with concepts such as model declarations, database queries, and so on

- ##### `Steps:`
    - Go in the `core/docs/` and copy the `example/` folder
    - In the main filesystem go in the `app/` folder and paste the copied folder
    - Modifiy the files `routes` / `models` / `handlers` / `apis` as you please

#

### Methods Coming Soon:

### Assisted creation:
This method helps you create a new application from scratch by guiding you through a customizable and easy-to-use configuration process for the application. It is also more accessible and easier to integrate compared to the other options.
- ##### `Requirements:`
    - there are no requirements needed to create a new application with this tool.

    - Note that this tool is not 100% accurate and may not satisfy prefectly what you have planned to do in the app
- ##### `Steps:`
    - Open the dashboard of cardinal by adding `/cardinal` after the base url.
    - Select from the menu `Applications`.
    - Select `New App` in the top right corner of the page
    - Go through all the configuration pages to customize the page and its functionalities
    - Save the result. A new application folder should be created in the `app/` folder
    - Check if the application has been successfully created by running the starting command for the application (see [here](https://example.com) for all the commands documentation)
#

