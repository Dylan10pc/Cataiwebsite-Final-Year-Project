This is a django project.(Please notw you will need to download the ai model from this link: https://drive.google.com/file/d/1GkV51guC1v-niSKk5rF3uHw1Ti64vWkQ/view?usp=sharing The model is too big to be on github) 
Just to let you know, there are more than just Django, so you will need to install those libraries too.

You must have a virtual environment to be able to run this effectively.

The Python version must be python 3.12.8

To install the virtual environment and connect it to the Django project, you will need a terminal or vscode and use its terminal. I used vs code but you can choose what is best for you.
How to install this venv is as followed:

Create the venv:
(Note you don't have to make the venv in the project dir, but its just easier)
1.OPEN A TERMINAL
Navigate to the django project directory in the terminal:
cd /path/to/project


2.Create the venv
python3.12 -m venv venv
that should download the venv


If by any chance that doesn't work, please use the full path
/path/to/python3.12.8 -m venv venv


3.activate the venv by doing this
venv\Scripts\activate
If activated, you should see venv at the start of your terminal


4.i have a requirements.txt, so it'll be easy to install dependencies
Put this in the terminal
pip install -r requirements.txt
if by any chance that doesn't work, you will need to install them manually one by one


5.Check if the dependencies are installed by doing
pip list


That should be everything for now to activate the venv


YOU WILL NOW NEED TO INSTALL THE MODEL FROM THIS LINK AS THE MODEL IS TOO LARGE TO BE ON GITHUB
https://drive.google.com/file/d/1GkV51guC1v-niSKk5rF3uHw1Ti64vWkQ/view?usp=sharing 
I need you to get this model. And drag it into 
![image](https://github.com/user-attachments/assets/43448f79-4dac-43f1-b4e0-b224f9a53bc7)



6.At this point, you could try
python manage.py runserver
if that doesnt work then follow these steps


7.Open vs Studio Code with the project
Press Ctrl + Shift + P and search for "Python: Select Interpreter".


8.Choose the venv in your project or wherever you made the venv (venv\Scripts\python.exe).
the project has the Python interpreter


9.Please do
python manage.py runserver
in VS Code


10.You may need to run manage.py first if a terminal isn't opened yet, 
and then do 
python manage.py runserver


11.Now open the link given to you by the terminal in your browser to check if the project is running



Ultimately, if nothing worked, you are free to call me and I am more than happy to help you set it up


