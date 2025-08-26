<h1 align="center">
  <img src="sphinx-doc/_static/images/logo_cpforager_text_color.png" alt="cpforager text logo with colors" width="600">
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
* `TDR_Collection` : for working with datasets composed of multiple TDR loggers.
* `AXY_Collection` : for working with datasets composed of multiple AXY loggers.

Each class automatically enhances raw data but also computes key features specific to each biologger (*e.g.* trip segmentation for GPS, dive segmentation for TDR, ODBA calculation for AXY). They are also accompanied with methods for data processing and visualisation.

<br>

<div align="center">
  <img src="sphinx-doc/_static/images/logo_cpforager_color.png" alt="cpforager logo with colors" width="200">
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

3. Open any Python script in [/tests/](./tests/) folder and start running line by line to check that everything is working.

4. Load your raw data in the [data/](./data/) folder, create your own script and enjoy !

<br>

# Documentation

The documentation of **cpforager** is automatically generated using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and can be found at [https://adrienbrunel.github.io/seabird-movement-cpf/](https://adrienbrunel.github.io/seabird-movement-cpf/).  

<!-- Using [Sphinx](https://www.sphinx-doc.org/en/master/index.html), the entire documentation of **cpforager** package is automatically generated with the following bash command lines :

```bash
cd sphinx-doc/
make clean
rm -rfv generated/
make html
```

The resulting html documentation is generated in the [/sphinx-doc/_build/html/](./sphinx-doc/_build/html/) folder. In order to browse the entire documentation, you just have to double-click on the [index.html](./sphinx-doc/_build/html/index.html) file. -->

<br>

# User guide 

The Python scripts in the [/tests/](./tests/) folder illustrate how the `GPS`, `TDR`, `AXY`, `GPS_TDR`, `GPS_Collection`, `TDR_Collection` and `AXY_Collection` classes can be used to fully benefit the users. Results of the scripts are also found in the [/tests/](./tests/) folder. For more details, you can browse the package [documentation](https://adrienbrunel.github.io/seabird-movement-cpf/).

<br>

# Future developments
- [ ] make classes' methods available in documentation.
- [ ] uniformise types of arguments/attributes in function arguments and accordingly in documentation.
- [ ] add a proper zero offset correction inside `TDR` class (according to a scientific consensus).
- [x] compute depth as a negative number to plot the visual depth.
- [x] improve `AXY_Collection` class.
- [x] improve `TDR_Collection` class.
- [ ] improve folium map of `GPS_Collection`.
- [x] add a plot_all method to the `GPS_Collection`, `AXY_Collection` and `TDR_Collection` that plot the raw data in separate plots.
- [ ] add a function `GPS_TDR = merge_gps_tdr(GPS, TDR)` that will merge TDR data within GPS data and produce the resulting dataframe.
- [ ] complete and improve `GPS_TDR` class.
- [ ] add a `GPS_TDR_Collection` class.
- [ ] add Butterworth filter for `AXY`.
- [ ] add parameters in `parameters.py` to be able to choose between rolling average and Butterworth filter for `AXY`.
- [x] automatically compute n_rows and n_columns for a given number of plots to display.
- [ ] hmmlearn for a 3-state estimation (foraging, traveling, resting).
- [ ] create first Github release / version 1.0. 
- [x] deploy documentation as a static webpage.
- [ ] build Python package [Python package building](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

<br>

# Infos
* Python version used is 3.13.3.
* OS used is Ubuntu 20.04.
* The graphic design of the logos was done by Lisa Brunel.