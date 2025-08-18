<h1 align="center">
  <img src="doc/_static/images/logo_cpforager_text_color.png" alt="cpforager text logo with colors" width="600">
</h1><br>

<div align="center">
  <a href="https://github.com/AdrienBrunel/seabird-movement-cpf/stargazers"><img alt="github stars" src="https://img.shields.io/github/stars/AdrienBrunel/seabird-movement-cpf"></a>
  <a href="https://github.com/AdrienBrunel/seabird-movement-cpf/forks"><img alt="github forks" src="https://img.shields.io/github/forks/AdrienBrunel/seabird-movement-cpf"></a>
  <a href="https://github.com/AdrienBrunel/seabird-movement-cpf/blob/master/LICENSE"><img alt="license" src="https://img.shields.io/badge/license-AGPLv3-blue"></a>
</div><br>

<br>

Are you a scientist involved in movement ecology working with biologging data collected from central-place foraging seabirds? **cpforager** is a Python package designed to help you manipulate, process, analyse and visualise the biologging datasets with ease.

<br>

The main objectives of **cpforager** are :  
1. Efficiently handle large-scale biologging datasets, including high-resolution sensor data (*e.g.* accelerometers).
2. Provide a modular and extensible architecture, allowing users to tailor the code to their specific research needs.
3. Facilitate a smooth transition to Python for movement ecology researchers familiar with other languages (*e.g.* R).

<br>

**cpforager** package supports various biologging sensor types commonly used in movement ecology and provides the following core classes:
* `GPS` : for handling position recordings. 
* `TDR` : for handling pressure recordings.
* `AXY` : for handling tri-axial acceleration recordings at high resolution combined with lower resolution position and pressure recordings.
* `GPS_TDR` : for handling position and pressure recordings.
* `GPS_Collection` : for working with datasets composed of multiple GPS loggers.
* (`TDR_Collection` : for working with datasets composed of multiple TDR loggers.)
* (`AXY_Collection` : for working with datasets composed of multiple AXY loggers.)

Each class automatically enhances raw data but also computes key features specific to each biologger (*e.g.* trip segmentation for GPS, dive segmentation for TDR, ODBA calculation for AXY). They are also accompanied with methods for data processing and visualisation.

<br>

<div align="center">
  <img src="doc/_static/images/logo_cpforager_color.png" alt="cpforager logo with colors" width="200">
</div>

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

3. Open any Python script in [tests/](./tests/) folder and start running line by line to check that everything is working.

4. Load your raw data in the [data/](./data/) folder, create your own script and enjoy !

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

The Python scripts in the [tests/](./tests/) folder illustrate how the `GPS`, `TDR`, `AXY` and `GPS_Collection` classes can be used to fully benefit the users. Results of the scripts are also found in the [tests/](./tests/) folder. For more details, you can browse the package documentation.

<br>

# Future developments
- [ ] make classes' methods available in documentation.
- [ ] uniformise types of arguments/atttributes in documentation.
- [ ] add Butterworth filter for `AXY`.
- [ ] add parameters in `parameters.py` to be able to choose between rolling average and Butterworth filter for `AXY`.
- [x] add functions that raise warnings (datetime order, datetime duplicates, interrupted trips, not normal datetime range, no trip found, not normal dataframe size, absent data, *etc.*).
- [ ] add a function `GPS_TDR = merge_gps_tdr(GPS, TDR)` that will merge TDR data within GPS data and produce the resulting dataframe.
- [ ] create a `AXY_Collection` class.
- [ ] create a `TDR_Collection` class.
- [x] clarify the purpose of `main.py` and thus folder `plots` and `results`.
- [x] rename `test` folder to `tests` folder.
- [ ] improve folium map of `GPS_Collection`.
- [ ] improve `GPS_TDR` class constructor.
- [x] create `pyproject.toml` file for [Python package building](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
- [ ] create first Github release / version 1.0. 

<br>

# Infos
* Python version used is 3.13.3
* OS used is Ubuntu 20.04