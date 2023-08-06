"""Data modules

This package contains image examples used in tutorials and notebooks.
"""

# Rem: images are stored in ".npy" format to avoid dependencies to PIL, ... (PIL may cause issues on Google Colab)

import numpy as np

import os

# Inspired by https://github.com/scikit-image/scikit-image/blob/master/skimage/data/__init__.py
data_dir = os.path.abspath(os.path.dirname(__file__))

__all__ = ['lst']

def lst():
    """An image from a simulated LST (Prod3b).

    Often used for tutorials and examples.

    This is the Whirlpool Galaxy, also known as M51 or NGC 5194.

    Sources
    -------

    - http://hubblesite.org/image/1038/news_release/2001-10
    - https://commons.wikimedia.org/wiki/File:Whirpool_Galaxy.jpg

    Returns
    -------
    one dimension ndarray
        LST image.
    """
    return np.load(os.path.join(data_dir, "lst.npy"))
