import re
import inspect
import functools
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

from .palettes import all_colors


__all__ = ['extract_palette', 'make_colormap', 'msme_colors']


def extract_palette(color_palette):
    """
    Extract color palette information and return a str/list of hex colors.

    Parameters
    ----------

    color_palette : str, list, or dict
        A color string, list of color strings, or color palette dict

    Returns
    -------
    colors : list
        Either a hex color or list of hex colors

    """
    if isinstance(color_palette, dict):
        colors = list(color_palette.values())
        if all(map(ishex, colors)):
            return colors
    elif isrgb(color_palette):
        return color_palette
    elif isinstance(color_palette, (list, tuple, np.ndarray)):
        if all(map(ishex, color_palette)):
            return color_palette
        elif all(map(isrgb, color_palette)):
            return color_palette
        elif all([color in all_colors.keys() for color in color_palette]):
            return [all_colors.get(color) for color in color_palette]
    elif isinstance(color_palette, str):
        color = all_colors.get(color_palette, None)
        if color:
            return color
        elif ishex(color_palette):
            return color_palette
    elif isinstance(color_palette, type(None)):
        return color_palette
    raise ValueError('Not a valid color string, list, or dictionary')


def make_colormap(color_palette, N=256, gamma=1.0):
    """
    Create a linear colormap from a color palette.

    Parameters
    ----------

    color_palette : str, list, or dict
        A color string, list of color strings, or color palette dict

    Returns
    -------
    cmap : LinearSegmentedColormap
        A colormap object based on color_palette using linear segments.

    """
    colors = extract_palette(color_palette)
    rgb = map(hex2rgb, colors)
    return LinearSegmentedColormap.from_list('custom', list(rgb),
                                             N=N, gamma=1.0)


def msme_colors(func):
    """
    A decorator function for enabling MSMExplorer colors.

    Parameters
    ----------

    func : function
        A plotting function

    Returns
    -------
    wrapper : function
        Modified plotting function

    """
    # Adapted from http://stackoverflow.com/questions/147816/preserving-signatures-of-decorated-functions
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inspect_kwargs = get_kwargs(func)
        kwargs.update([(k, extract_palette(kwargs.get(k, v)))
                       for k, v in kwargs.items() if 'color' in k])
        if inspect_kwargs:
            kwargs.update([(k, extract_palette(kwargs.get(k, v)))
                           if 'color' in k else (k, kwargs.get(k, v))
                           for k, v in inspect_kwargs.items()])
        return func(*args, **kwargs)
    return wrapper


def get_kwargs(func):
    # Adapted from http://stackoverflow.com/questions/196960/can-you-list-the-keyword-arguments-a-python-function-receives
    args, _, _, defaults = inspect.getargspec(func)
    if defaults:
        kwargs = args[-len(defaults):]
        return dict(zip(kwargs, defaults))
    return None


def ishex(color):
    # Adapted from http://stackoverflow.com/questions/30241375/python-how-to-check-if-string-is-a-hex-color-code
    match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', str(color))

    if match:
        return True
    return False


def isrgb(color):
    return (isinstance(color, (tuple, list, np.ndarray)) and
            (len(color) == 3 or len(color) == 4) and
            all([isinstance(item, (float, int)) for item in color])
            )


def hex2rgb(color):
    # Adapted from http://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python

    h = color.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255. for i in (0, 2, 4))
