""" ``sklearn_xarray`` """

from sklearn_xarray.common.wrappers import (
    wrap, EstimatorWrapper, ClassifierWrapper, RegressorWrapper,
    TransformerWrapper)
from sklearn_xarray.target import Target

from sklearn_xarray.version import __version__, __release__

import os


__all__ = [
    'wrap',
    'EstimatorWrapper',
    'ClassifierWrapper',
    'RegressorWrapper',
    'TransformerWrapper',
    'Target'
]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
