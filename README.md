# cpforager

<div align="center">
  <a href="https://github.com/AdrienBrunel/seabird-movement-cpf/stargazers"><img alt="stars" src="https://img.shields.io/github/stars/AdrienBrunel/seabird-movement-cpf"></a>
  <a href="https://github.com/AdrienBrunel/seabird-movement-cpf/forks"><img alt="forks" src="https://img.shields.io/github/forks/AdrienBrunel/seabird-movement-cpf"></a>
  <a href="https://github.com/AdrienBrunel/seabird-movement-cpf/blob/master/LICENSE"><img alt="license" src="https://img.shields.io/badge/license-AGPLv3-blue"></a>
</div>

<br>

Are you a scientist involved in movement ecology working with biologging data collected from central-place foraging seabirds? **cpforager** is a Python package designed to help you manipulate, process, analyse and visualise the biologging datasets with ease.

<br>

The main objectives of **cpforager** package are :  
1. Efficiently handle large-scale biologging datasets, including high-resolution sensor data (*e.g.* accelerometers).
2. Provide a modular and extensible architecture, allowing users to tailor the code to their specific research needs.
3. Facilitate a smooth transition to Python for movement ecology researchers familiar with other languages (*e.g.* R).

<br>

**cpforager** package supports various biologging sensor types commonly used in the field and provides the following core classes:
* `GPS` : for handling position recordings. 
* `TDR` : for handling pressure recordings.
* `AXY` : for handling tri-axial acceleration recordings at high resolution combined with lower resolution position and pressure recordings.
* `GPS_Collection` : for working with datasets composed of multiple GPS loggers.
* (`TDR_Collection` : for working with datasets composed of multiple TDR loggers.)
* (`AXY_Collection` : for working with datasets composed of multiple AXY loggers.)

Each class automatically enhances raw data but also computes key features specific to each biologger (*e.g.* trip segmentation for GPS, dive segmentation for TDR, ODBA calculation for AXY). They are also accompanied with built-in methods for data processing and visualisation.

<br>
<br>

# Installation

1. Clone this repository on your local machine :
```bash
git clone https://github.com/AdrienBrunel/seabird-movement-cpf
```

2. Create a conda environment using the [environment.yml](environment.yml) file :
```bash
conda env create --name seabird-movement-cpf --file environment.yml
```

3. Open the [main.py](main.py) or [test.py](./test/test.py) file and start running line by line to check that everything is working.

4. Load your raw data in the [data/](./data/) folder,  create your own script and enjoy :) 

<br>

# Documentation

Using [Sphinx](https://www.sphinx-doc.org/en/master/index.html), the entire documentation of **cpforager** package is automatically generated with the following command lines :

```bash
cd doc/
make clean
rm -rfv generated/
make html
```

The resulting html documentation is generated in the [./doc/_build/html/](./doc/_build/html/) folder. In order to browse the entire documentation, you just have to double-click on the [index.html](./doc/_build/html/index.html) file.

<br>

# User guide 

The script [test.py](./test/test.py) illustrates how the `GPS`, `TDR`, `AXY` and `GPS_Collection` classes should be used to fully benefit the users. Results of the methods called within the script are found in the [test](./test/) folder. For more details, you can browse the package documentation.

<br>

# Future developments
- [ ] improve documentation (add images of test results, uniformize, add logo)
- [ ] create a function `merge_gps_tdr(GPS, TDR)` that will merge TDR data within GPS data and produce the resulting dataframe.
- [ ] create a `GPS_TDR` class for biologgers with both GPS and TDR data.
- [ ] create a `AXY_Collection` class.
- [ ] create a `TDR_Collection` class.
- [ ] add a test block where gps data is cutted by trip and written as csv.
- [ ] add a test block where gps data are read from SeabirdTracking Database.
- [ ] add a method to_SeabirdTracking() in `GPS_Collection`.
- [ ] add a `fast=True` argument to the full_diag() method of `AXY`.
- [ ] find out how fully benefit from `GPS` and `TDR` methods in `AXY` (*e.g.* display, diagnostic).
- [ ] nb_dives --> n_dives and n_trip --> n_trips.
- [ ] correction associated to remove_suspicious() bug in `AXY`.
- [ ] emphasize dives on the GPS_TDR plots.

<br>

# Infos
* Python version used is 3.13.3
* OS used is Ubuntu 20.04
* Environment can be loaded using [environment.yml](environment.yml)
