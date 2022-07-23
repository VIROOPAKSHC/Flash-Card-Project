## This file tells you details to run the code in local setting
Download the files using:
```
git clone https://github.com/VIROOPAKSHC/Flash-Card-Project.git local-folder-name
```
or
```
git clone https://github.com/VIROOPAKSHC/Flash-Card-Project.git
```
Now navigate to the folder and open Linux Shell or Windows Command prompt there.<br>
<br>
Create a virtual environment using:<br>

```
python3 -m venv /path/to/new/virtual/environment
```

Let the name of the virtual environment you have created is venv and discuss on how to run the code further.<br>
After creating the virtual environment we need to activate the environment:<br>
```
venv\Scripts\activate
```
in Windows and <br>
```
source venv/Scripts/activate
```
in Linux or Ubuntu or WSL shell <br>
<br>
After activating the virtual environment, install dependencies using:<br>
```
pip install -r requirements.txt
```
<br>
Run the code using:
```
python main.py
```
or
```
python3 main.py
```
different from the usual ```flask run``` or ```set FLASK_APP=...```
<br>
If there is a module not found error raised install the module using: ```pip install <module-name>``` and try running again. Everything should work fine.
