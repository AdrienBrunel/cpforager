<h1 align="center">
  <img src="https://github.com/AdrienBrunel/cpforager/raw/master/docs/_static/images/logo_cpforager_text_color.png" alt="cpforager text logo with colors" width="600">
</h1><br>

<div align="center">
  <a href="https://github.com/AdrienBrunel/cpforager/stargazers"><img alt="github stars" src="https://img.shields.io/github/stars/AdrienBrunel/cpforager"></a>
  <a href="https://github.com/AdrienBrunel/cpforager/forks"><img alt="github forks" src="https://img.shields.io/github/forks/AdrienBrunel/cpforager"></a>
  <a href="https://github.com/AdrienBrunel/cpforager/issues"><img alt="github issues" src="https://img.shields.io/github/issues/AdrienBrunel/cpforager"></a>
  <a href="https://github.com/AdrienBrunel/cpforager/pulls"><img alt="github pull request" src="https://img.shields.io/github/issues-pr/AdrienBrunel/cpforager"></a>
  <a href="https://github.com/AdrienBrunel/cpforager/commits/main"><img alt="github last commit" src="https://img.shields.io/github/last-commit/AdrienBrunel/cpforager"></a>
</div>
<div align="center">
  <a href="https://github.com/AdrienBrunel/cpforager/blob/master/LICENSE"><img alt="license" src="https://img.shields.io/badge/license-AGPLv3-blue"></a>
  <a href="https://www.python.org/downloads/"><img alt="python 3.11+" src="https://img.shields.io/badge/Python-3.11+-blue.svg"></a>
</div>
<div align="center">
  <a href="https://badge.fury.io/py/cpforager"><img alt="pypi version" src="https://badge.fury.io/py/cpforager.svg"></a>
  <a href="https://pypi.org/project/cpforager/"><img alt="pypi downloads" src="https://img.shields.io/pypi/dm/cpforager.svg"></a>
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

**cpforager** also allows to deal with a list of sensors using the following classes:
* `GPS_Collection` : for working with datasets composed of multiple GPS loggers.
* `TDR_Collection` : for working with datasets composed of multiple TDR loggers.
* `AXY_Collection` : for working with datasets composed of multiple AXY loggers.
* `GPS_TDR_Collection` : for working with datasets composed of multiple GPS_TDR loggers.

Each class automatically enhances raw data but also computes key features specific to each biologger (*e.g.* trip segmentation for GPS, dive segmentation for TDR, ODBA calculation for AXY). They are also accompanied with methods for data processing and visualisation.

<br>

<div align="center">
  <img src="https://github.com/AdrienBrunel/cpforager/raw/master/docs/_static/images/logo_cpforager_color.png" alt="cpforager logo with colors" width="200">
</div>

<br>