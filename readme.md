# Starcraft Clustering

This project performs clustering on starcraft build orders

# Folder Structure

    .
    ├── Data                    # Input replay files, all subfolders will be traversed
    ├── docs                    # Folder for more documentation
    ├── src                     # Source Code
    ├── test                    # Test Cases
    ├── build.orders            # Preprocessed build orders stored here 
    ├── levenshtein             # precomputed levenshtein distances stored here
    ├── venv                    # Convenient location for python virtual environment
    ├── dendrograms             # Output diretory, contains clustering diagrams
    └── test.data               # Data associated with test cases


# Replay Files

Additional replay files can be found here

https://lotv.spawningtool.com/replaypacks/


# Clustering 

This Project uses [OPTICS](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html) clustering


Since Starcraft build orders are not numbers, [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance) distance is used as a distance metric, to measure the distance between two build orders. 


# Running it

You will need to install [python](https://www.python.org/downloads/)

Check out the repo

```bash
git clone https://github.com/sav-chris/Starcraft-Clustering.git
```

`setup.bat` is the script that creates a virtual environment and installs the dependencies.
On windows you can run this, if you are on linux run `setup.sh`

If you have already run this, you just need to activate the virtual environment

on windows

```bash
.\venv\Scripts\activate
```

on linux

```bash
source venv/bin/activate
```

You will need to get some replay files such as the ones available on [spawning tool](https://lotv.spawningtool.com/replaypacks/)

Unzip them into the `Data` folder. They may be in subfolders as all subfolders will be searched.

To run the whole thing:

Go to src folder
```bash
cd src
```

```bash
python clustering.py
```

# Running test cases

Once you have created and activated your virtual environment, you can run the test cases.

Go to test folder
```bash
cd test
```

Each test file is run individually, ie:
```bash
python ClusteringController.test.py
python LabelEncoder.test.py
python Player.test.py
python RaceBuildOrder.test.py
```

# Dendrograms 

The program output is stored in the `Dendrongrams` folder.

Each run is stored in a new subfolder and the `Hyperparameters.json` file records the selected hyperparameters used for that run.

The files `Race.Protoss.Uncategorised.txt`,  `Race.Terran.Uncategorised.txt` and `Race.Zerg.Uncategorised.txt` record the number of build orders that were not assigned to a cluster for their respective races.   

The dendrogram images will be stored in [svg](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) files and look like this:

![Example Dendrogram](docs/example%20dendrogram.png)

