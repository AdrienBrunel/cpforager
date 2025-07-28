# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "cpforager"
copyright = "2025, Adrien Brunel"
author = "Adrien Brunel"
version = "0.0"
release = "0"
language = "en"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
templates_path = ["../doc/_templates"]
exclude_patterns = ["../doc/_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"


# -- Authorized extensions -------------------------------------------------
# authorized extensions
extensions = ["sphinx.ext.duration",
              "sphinx.ext.doctest",
              "sphinx.ext.autodoc",
              "sphinx.ext.autosummary"]


# command line for building documentation : sphinx-build -M html src/ doc/ -c doc/
# command line for building documentation : make html
