## Running the Models and Visualizations:

### Step 1:

Ensure python 3 is installed.

### Step 2:

Create a virtual environment for the models. In a terminal window, navigate to the project directory and run one of the following commands or skil or skip to step 3 if you wish to use the same environment for the other project components:

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

Note: to deactivate the environment, type the following into the terminal:
```bash
deactivate
```

### Step4:

Within the models directory run the following command to install the required packages:
```bash
pip install -r requirements.txt
```

### Step5:

If you wish to run the jupyter notebooks by code blocks open jupyter notebooks or your desired IDE and hit run all.

If you wish to run the jupyer notebooks by within the terminal run the following command (modify file_name to the desired notebook name):
```bash
jupyter nbconvert --to script --stdout file_name.ipynb | python
```

NOTE: Running notebooks requires access to the data as formatted within each notebook

In each Jupyter Notebook there is a data_dir variable to change to the local directory holding the data
The Data folder should be structured as followed:
```
project-root/
│
├── data/
│   │
│   ├── control/
│   │   ├── session_2/
|   |   |   └── video.mpk
|   |   |   └── raw_emotibit.csv
|   |   |   └── hr.csv
|   |   |   └── timestamp.csv
|   |   |   └── tracking.csv
│   │   └── session_3/
│   │
│   ├── participants/
│   │   ├── session_2/
|   |   |   └── video.mpk
|   |   |   └── raw_emotibit.csv
|   |   |   └── hr.csv
|   |   |   └── timestamp.csv
|   |   |   └── tracking.csv
│   │   └── session_3/
```