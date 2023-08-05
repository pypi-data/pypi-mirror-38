# -*- coding: utf-8 -*-
""" Loading configuration file

LDT has a number of module-wide variables for default parameters. They can
also be overridden in most modules when instantiating resource objects. See
tutorial for explanation of parameters and a sample.

"""

import os
import warnings
import sys
import shutil
import ruamel.yaml as yaml
import outdated

from ldt.helpers.exceptions import ResourceError
from ldt._version import __version__

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

from outdated import warn_if_outdated

warn_if_outdated('ldt', __version__)

# downloading NLTK resources if they're missing
# if not "unittest" in sys.modules or "sphinx" in sys.modules:
#     nltk.download("wordnet")
#     nltk.download("stopwords")
#     nltk.download("punkt")

TESTFILE = os.path.dirname(os.path.realpath(__file__))
TESTFILE = os.path.join(TESTFILE, "tests/sample_files/.ldt-config.yaml")

if "unittest" in sys.modules or "sphinx" in sys.modules:
    CONFIGPATH = TESTFILE
else:
    CONFIGPATH = os.path.expanduser('~/.ldt-config.yaml')
    if not os.path.exists(CONFIGPATH):
        print("Creating a sample configuration file in", CONFIGPATH)
        shutil.copyfile(TESTFILE, CONFIGPATH)

def load_config(path=CONFIGPATH):
    """Loading config file from either the user home directory or the test
    directory"""
    print("Loading configuration file:", path)
    if not os.path.isfile(path):
        raise ResourceError("Configuration yaml file was not found at "+path)

    with open(path) as stream:
        try:
            options = yaml.safe_load(stream)
        except yaml.YAMLError:
            raise ResourceError("Something is wrong with the configuration "
                                "yaml file.")

    if "unittest" in sys.modules:
        options["path_to_resources"] = TESTFILE.strip(".ldt-config.yaml")
        options["experiments"]["embeddings"] = \
            [os.path.join(options["path_to_resources"], "sample_embeddings")]
        options["wiktionary_cache"] = False
        options["experiments"]["top_n"] = 2
        options["experiments"]["batch_size"] = 2
        options["experiments"]["timeout"] = None
        options["experiments"]["multiprocessing"] = 1
        options["corpus"] = "Wiki201308"
    options["path_to_cache"] = \
        os.path.join(options["path_to_resources"], "cache")
    for i in options:
        if options[i] == "None":
            options[i] = None

    return options

#pylint: disable=invalid-name
global config
config = load_config()

# def update_config(new_config_path):
#     """Updating the config with the contents of an alternative yaml file."""
#     if not os.path.isfile(new_config_path):
#         print("Path not found: ", new_config_path)
#         return None
#     with open(new_config_path) as stream:
#         try:
#             new_config = yaml.safe_load(stream)
#             return new_config
#         except:
#             print("Something is wrong with the configuration yaml file: ",
#                   new_config_path)

