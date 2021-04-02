# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys

# SET CURRENT_VERSION
from git import Repo

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
# At top on conf.py (with other import statements)
from recommonmark.transform import AutoStructify


# At the bottom of conf.py
def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            #'url_resolver': lambda url: github_doc_root + url,
            "auto_toc_tree_section": "Contents",
            "enable_math": False,
            "enable_inline_math": False,
            "enable_eval_rst": True,
        },
        True,
    )
    app.add_transform(AutoStructify)


sys.path.insert(0, os.path.abspath("../.."))
sys.path.insert(0, os.path.abspath("../../pidroidbot_discord"))

# -- Project information -----------------------------------------------------

project = "pidroidbot-discord"
copyright = "2021, PiDroid-B"
author = "PiDroid-B"

# The short X.Y version
version = "v0.0.1"

# The full version, including alpha/beta/rc tags
release = "v0.0.6"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "recommonmark",
    "sphinx.ext.autosectionlabel",
]

autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------
epub_exclude_files = ["search.html"]

autosectionlabel_prefix_document = True

############################
# SETUP THE RTD LOWER-LEFT #
############################
try:
    html_context
except NameError:
    html_context = dict()
html_context["display_lower_left"] = True

if "REPO_NAME" in os.environ:
    REPO_NAME = os.environ["REPO_NAME"]
else:
    REPO_NAME = ""

# SET CURRENT_LANGUAGE
if "current_language" in os.environ:
    # get the current_language env var set by buildDocs.sh
    current_language = os.environ["current_language"]
else:
    # the user is probably doing `make html`
    # set this build's current language to english
    current_language = "en"

# tell the theme which language to we're currently building
html_context["current_language"] = current_language


repo = Repo(search_parent_directories=True)

if "current_version" in os.environ:
    # get the current_version env var set by buildDocs.sh
    current_version = os.environ["current_version"]
else:
    # the user is probably doing `make html`
    # set this build's current version by looking at the branch
    current_version = repo.active_branch.name

# tell the theme which version we're currently on ('current_version' affects
# the lower-left rtd menu and 'version' affects the logo-area version)
html_context["current_version"] = current_version
html_context["version"] = current_version

# POPULATE LINKS TO OTHER LANGUAGES
html_context["languages"] = [("en", "/" + REPO_NAME + "/en/" + current_version + "/")]

languages = [lang.name for lang in os.scandir("locales") if lang.is_dir()]
for lang in languages:
    html_context["languages"].append(
        (lang, "/" + REPO_NAME + "/" + lang + "/" + current_version + "/")
    )

# POPULATE LINKS TO OTHER VERSIONS
html_context["versions"] = list()

versions = [branch.name for branch in repo.branches]
for version in versions:
    html_context["versions"].append(
        (version, "/" + REPO_NAME + "/" + current_language + "/" + version + "/")
    )

# POPULATE LINKS TO OTHER FORMATS/DOWNLOADS

# settings for creating PDF with rinoh
rinoh_documents = [
    (master_doc, "target", project + " Documentation", "© " + copyright,)
]
today_fmt = "%B %d, %Y"

# settings for EPUB
epub_basename = "target"

html_context["downloads"] = list()
html_context["downloads"].append(
    (
        "pdf",
        "/"
        + REPO_NAME
        + "/"
        + current_language
        + "/"
        + current_version
        + "/"
        + project
        + "-docs_"
        + current_language
        + "_"
        + current_version
        + ".pdf",
    )
)

html_context["downloads"].append(
    (
        "epub",
        "/"
        + REPO_NAME
        + "/"
        + current_language
        + "/"
        + current_version
        + "/"
        + project
        + "-docs_"
        + current_language
        + "_"
        + current_version
        + ".epub",
    )
)
