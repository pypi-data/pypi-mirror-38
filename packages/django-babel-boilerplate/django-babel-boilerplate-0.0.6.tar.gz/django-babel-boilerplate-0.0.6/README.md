# Django Babel Package

This is a package to create a boilerplate of django and babel with a efficient method of file structure

# GET STARTED

In your terminal run the command..

``$ pip install django-babel-boilerplate``

To create a project,

``$ django-babel [project_name]``

The file structure would look like

- [root-folder]
    - settings
        - base.py
        - local.py
        - production.py
        - staging.py
    - \_\_init\_\_.py
    - urls.py
    - views.py
    - wsgi.py
- static
    - common
        - js
        - scss
    - dist
        - css
        - images
        - js
    - home
        - js
        - scss
    - svg
- templates
    - index.html
- .babelrc
- .gitignore
- manage.py 
- package.json
- requirements-server.txt
- requirements.txt

To install all the dependencies.

``$ npm install``

To run just the server 

``$ python manage.py runserver``

or

``$ npm start server``

To run babel, use 

``$ npm start babel``

To run the sass, use

``$ npm start scss``

To run the server, babel and the sass all together, use 

``$ npm start``

Your good to go..

Happy Coding :)