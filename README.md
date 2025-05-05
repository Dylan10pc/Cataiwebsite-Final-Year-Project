This is a django project.
be aware that there are more than just django so you will need to install those libaries too.

You must have a virtual env to be able to run this effectively.

The python version must be python 3.12.8

To install the virtual enviroment and connect it to the django project you will need a terminal or vscode and use its terminal. I used vs code but you can choose what is best for you.
How to install this venv is as followed:

Create the venv:
(note you dont have to make the venv in the project dir but its just easier)
Navigate to the django project dir in the terminal doing.
cd /path/to/project

The create the venv
python3.12 -m venv venv
that should download the venv

if by any chnace that doesnt work please do using the full path
/path/to/python3.12.8 -m venv venv

activate the venv by doing this
venv\Scripts\activate
if activated you should see venv at the start of your terminal

i have a requirements.txt so itll be easy to install dependicies
put this in the terminal
pip install -r requirements.txt
if by any chnace that doesnt work you will need to install them manually one by one

check if the dependcies installed by doing
pip list

That shouls be everything for now 
to activate the venv for the project now

at this point you could try
python manage.py runserver
if that doesnt work then follow these steps

open vs studio code with the project
Press Ctrl + Shift + P and search for "Python: Select Interpreter".

Choose the venv located in your project or whereveer you made the venv (venv\Scripts\python.exe).

OR

at the bottom there may be a button to let you auto set the inpreter if not please ignore this.

once the project has the python inpreter

please do
python manage.py runserver
in vs code

you may need to run manage.py first if a terminal isnt opened yet 
and then do 
python manage.py runserver

Now open http://127.0.0.1:8000/ in your browser to check if the project is running



ultimately if nothing worked you are free to call me and I am more than happy to help you set it up


