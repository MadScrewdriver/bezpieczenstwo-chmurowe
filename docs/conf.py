import os
import sys
import django

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bezpieczeństwo Chmurowe'
copyright = '2025, Daniel Pietruczyk, Franciszek Łajszczak, Kacper Malik, Ola Lewandowska'
author = 'Daniel Pietruczyk, Franciszek Łajszczak, Kacper Malik, Ola Lewandowska'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

latex_elements = {
    'babel': '\\usepackage[polish]{babel}',
    'inputenc': '',  # w nowszym LaTeX domyślnie UTF-8
    'fontenc': '\\usepackage[T1]{fontenc}',
    'utf8extra': '',
}

latex_documents = [
    ('index', 'django_doc.tex', 'Dokumentacja Kodu',
     'Daniel Pietruczyk, Franciszek Łajszczak, Kacper Malik, Ola Lewandowska', 'manual'),
]


language = 'pl'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bezpieczenstwo_chmurowe.settings'

django.setup()
