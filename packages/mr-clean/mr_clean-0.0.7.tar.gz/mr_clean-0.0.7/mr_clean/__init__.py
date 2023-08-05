# -*- coding: utf-8 -*-
import warnings

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

__all__ = ['_utils','functions','main','stats']
dependencies = ['pandas','numpy']
missing_dependencies = []

for dependency in dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError("Missing required dependencies {0}".format(missing_dependencies))
del dependencies, missing_dependencies, dependency
# del
# del


from mr_clean.core.api import *

del warnings
