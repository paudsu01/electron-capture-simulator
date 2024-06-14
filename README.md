# Electron Capture Visual Simulator

## Introduction
This small project was done as part of Luther College's physics research under Prof. James Perez. The main research involves studying single electron capture by bare ions from a target nucleus. This project was done to help visualise this electron capture process. The visualization is done with the help of the `VPython` module.

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

## Note to people who setup Virtual Environment 
If you installed with `Method 2`, you will need to remember to activate your virutal env before running the program and deactivating once you are done.
1. To activate, first open up your terminal and navigate inside the project folder.
2. If you are a MAC/linux user type:
```bash
source .venv/bin/activate
```
in your terminal to activate the virtual env.

3. If you are a windows user type:
```bat
.venv\Scripts\activate.bat
```
in your terminal to activate the virtual env.

4. Type
```bat
deactivate
```
to deactivate the virtual environment for windows/Mac/Linux.

## What files are required to run the program?

1. <i><b>Coordinates `.dat` file </b></i> : Before running the program, you will need a `.dat` file with coordinate information for the projectile, electron and the target nucleus along with the time information. The `.dat` file should have 10 columns of information in the order mentioned below:
   
| Projectile x | Projectile y | Projectile z | TargetNucleus x | TargetNucleus y | TargetNucleus z | Electron x | Electron y | Electron z | Atomic Time
|-|-|-|-|-|-|-|-|-|-|

2. Consult `sample/coordinatesSample.dat` as an example of a coordinate `.dat` file.
   <hr></hr>
3. <i><b>Energy `.dat` file </b></i> If you wish to plot a graph while the simulation runs, you will also need Energy `.dat`  file with 2 columns of data.
5. The first column should contain `Electron's energy w.r.t Projectile` and the second column should contain `Electron's energy w.r.t Nucleus`
6. The graph will have the energy data in the y-axis against simulation time in the x-axis.
7. Consult `sample/energySample.dat` as an example of an energy `.dat` file.

## How to run the program ?

Inside the `sample` folder, there are two files : `coordinatesSample.dat` and `energySample.dat`. You can try using these files to get started with running the program. Open up a terminal, navigate to the root folder of this project, activate your virtual environment if you setup a virtual environment at the time of installation and type the following:

* To run the program in no-graph mode : 

```bash
python3 main.py sample/coordinatesSample.dat
```

* To run the program in interactive graph mode :
  
```bash
python3 main.py sample/coordinatesSample.dat sample/energySample.dat
```

* To run the program in non interactive fast graph mode :
  
```bash
python3 main.py sample/coordinatesSample.dat sample/energySample.dat -f
```

## Why open source ?

This project is specifically tailored for Prof Perez's research and will probably not serve use to anyone outside his research group.
The reason this is open-source is so that other students working with Prof Perez can access this repository and use the documentation and other resources to get started with running the program.

