# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "seabird-movement-cpf"
copyright = "2025, Adrien Brunel"
author = "Adrien Brunel"
version = "0.0"
release = "0"
language = "en"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["../doc/_templates"]
exclude_patterns = ["../doc/_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "classic"
# html_static_path = ["../doc/_static"]

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
#html_theme = 'sphinxdoc'



# -- Authorized extensions -------------------------------------------------
# authorized extensions
extensions = ["sphinx.ext.duration",
              "sphinx.ext.doctest",
              "sphinx.ext.autodoc",
              "sphinx.ext.autosummary"]


# command line for building documentation : sphinx-build -M html src/ doc/ -c doc/
