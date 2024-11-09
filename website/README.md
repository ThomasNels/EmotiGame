## Running the website:

### Step 1: 
Ensure python 3 is installed.

### Step 2:
Create a virtual environment for the website. In a terminal window, navigate to the project directory and run one of the following commands:

Windows:
```bash
python -m venv <environment name>
```

macOS and Linux:
```bash
python3 -m venv <environment name>
```

### Step 3:
Active the virtual environment using one of the following commands in the terminal at the project directory:

Windows:
```bash
<environment name>\Script\activate
```

macOS and Linux:
```bash
source <environment name>/bin/activate
```

Note: to deactivate the environment, type 
```bash
deactivate
``` 
into the the terminal.

### Step4:
Run the following command to install the required packages.
```bash
pip intall -r requirements.txt
```

### Step5:
Within the project directory type the following commands to run the application.
```bash
cd website
python3 app.py
```

To access the webpage, enter the follwing url:
```
localhost:5000
```
