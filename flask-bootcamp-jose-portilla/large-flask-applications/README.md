# Working with Large Flask Applications

Working again with the Adoption Site Project I will slice the *app.py* into little .py files inside a more complex directory structure 
kinda like a large Flask application should be and work with **blueprints** to handle the relationship of the structure.


## Structure Skeleton to follow:

├───app.py # main app.py file to be called to start server for web app
├───requirements.txt # File of pip install statements for your app
├───migrations # folder created for migrations by calling
├───myproject # main project folder, sub-components will be in separate folders
│   │   data.sqlite
│   │   models.py
│   │   \__init__.py
│   │
│   ├───owners
│   │   │   forms.py
│   │   │   views.py
│   │   │
│   │   ├───templates
│   │      └───owners
│   │             add_owner.html
│   │   
│   │
│   ├───puppies
│   │   │   forms.py
│   │   │   views.py
│   │   │
│   │   ├───templates
│   │   │   └───puppies
│   │   │           add.html
│   │   │           delete.html
│   │   │           list.html
│   │
│   ├───static # Where you store your CSS, JS, Images, Fonts, etc...
│   ├───templates
│          base.html
│          home.html