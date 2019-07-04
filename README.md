# CRB_Weather_app
Supporting python scripts to parse NAM grib data for use in the Crop Residue Burning website of Manitoba Agriculture. This readme will teach
you how to install the program in your computer for development purposes. Before completing the steps below, install the latest PyCharm Community Edition and create/activate the py27 
environment. Please refer to the Daily-Data-Upload Job Aid.

## Cloning the Repository

### 1. Install required Python Packages

1. Search and open Anaconda Prompt (py27).

2. Navigate using cd commands until you're inside the Project_Directory folder. 

* For example: 
```
cd C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory
```
3. Finally, type ```pip install -r REQUIREMENTS.txt``` and press Enter

### 2. Install GitGui and GitBash

1. Navigate to ```https://git-scm.com/download/win```

2. Double click the Git .exe file to start the installation.

3. If prompted, choose Nano as the default Git editor.

4. If prompted, choose 'Use Git from the Windows Command Prompt'

5. If prompted, choose 'Use Windows default console window'

6. If prompted, leave the 'Configuring extra options' menu in its default state and click 'Install'.

### 3. Clone Repository using Git
There are two ways to do this: through github.com and through Git Bash. The Git Bash method is recommended as it is less
of a hassle when you want upload your changes to GitHub.

#### Git Bash method (Recommended)

1. Create a folder to contain the contents of CRB_Weather_app.

2. Using windows search, find and open Git Bash.

3. At the Git Bash terminal, use cd commands to navigate to the folder you created in step 1.

* For example:
```
cd C:\Users\CAmao\Documents\NEW_FOLDER
```

4. Type ```git clone https://github.com/charleamaoAGR/CRB_Weather_app.git``` and press Enter. Note: Make sure you are outside of the
managed environment when completing this step.

#### GitHub.com method

1. Navigate to https://github.com/charleamaoAGR/CRB_Weather_app.

2. Click the green 'Clone or download' dropdown button and press Download Zip.

3. Extract the Zip file to your desired directory.

## Maintaining the Repository

