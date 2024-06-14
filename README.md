# Electron Capture Visual Simulator

## Introduction
This small project was done as part of Luther College's physics research under Prof. James Perez. The main research involves studying single electron capture by bare ions from a target nucleus. This project was done to help visualise this electron capture process.

## Installation guide
1. Install python on your computer/workstation if you haven't already.
2. Go to the main page of this repository. To the right of the list of files, click Releases.
3. Download the source code file of the latest released version.
4. Unzip the zipped file and navigate inside the folder in your terminal using the `cd` command.
5. Follow either `Method 1` or `Method 2` to download the required python packages. `Method 1` will make it easier to use the program but will install all python packages globally while `Method 2` will setup a python virtual environment but will require an extra step before running the program. I recommend `Method 2`.  
6. Navigate to `How to run` section after you are done with installation.

>Method 1

* Once you are inside the folder in the terminal , type the following:
```bash
pip install -r requirements.txt
```
* You are done with installation.

>Method 2

* MAC/Linux users : Once you are inside the folder in the terminal , type the following:
```bash
python3 -m venv .venv --prompt=ElectronCaptureSim
source .venv/bin/activate
pip install -r requirements.txt
```
* Window users with cmd.exe:
  
```bat
python -m venv .venv --prompt=ElectronCaptureSim
.venv\Scripts\activate.bat
pip install -r requirements.txt
```
* You are done with installation.

## How to run?

## Run the program with a sample file

## Why open source ?

This project is specifically tailored for Prof Perez's research and will probably not serve use to anyone outside his research group.
The reason this is open-source is so that other students working with Prof Perez can access this repository and use the documentation and other resources to get started with running the program.

## Contributing

