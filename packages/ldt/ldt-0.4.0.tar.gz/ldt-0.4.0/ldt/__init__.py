# -*- coding: utf-8 -*-
""" Initializing the ldt package

Subpackages
===========

.. autosummary::
    :toctree: _autosummary

"""

from ._version import __version__
from ldt.load_config import config

from ldt import helpers
from ldt.helpers.loading import load_resource

from ldt import dicts
from ldt import relations
from ldt.relations import Word
from ldt.relations import RelationsInPair

from ldt import experiments
