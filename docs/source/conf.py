import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


project = 'Contacts API'
copyright = '2025, Viacheslav Mykhailov'
author = 'Viacheslav Mykhailov'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_typehints = "description"
autodoc_preserve_defaults = True

