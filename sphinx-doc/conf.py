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
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"] 
max_line_length = 120

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinx_rtd_theme"

# customized css
def setup(app):
    app.add_css_file("css/style.css")

# logo
html_logo = "_static/images/logo_cpforager_text_color.png"
html_title = "cpforager"
html_favicon = "_static/images/logo_cpforager_color.png"
html_theme_options = {"logo_only": True}
    
# -- Authorized extensions -------------------------------------------------
extensions = ["sphinx.ext.duration",
              "sphinx.ext.doctest",
              "sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.todo"]

todo_include_todos = True

# command line for building documentation : 
# make clean
# rm -rfv generated/
# make html
# sphinx-pdf-generate doc/ doc/_build/html
