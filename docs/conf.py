# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'wwPDB Config Utilities'
copyright = '2025, wwPDB'
author = 'wwPDB'
release = 'unknown'

import sys
from pathlib import Path

sys.path.insert(0, str(Path('..').resolve()))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.napoleon',
#              "sphinx_autodoc_typehints", # must be after napolean
              'sphinx.ext.intersphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# python3 -m sphinx.ext.intersphinx https://docs.python-requests.org/en/master/objects.inv
intersphinx_mapping = {
    'requests': ('https://docs.python-requests.org/en/master/', None),
    'python': ('https://docs.python.org/3', None)
}
