from matplotlib.colors import Colormap

from ..palettes import msme_rgb
from ..utils import extract_palette, make_colormap, msme_colors


def test_extract_palette():
    assert extract_palette(msme_rgb) == list(msme_rgb.values())
    assert extract_palette(list(msme_rgb.keys())) == list(msme_rgb.values())
    assert extract_palette(list(msme_rgb.values())) == list(msme_rgb.values())
    assert extract_palette('beryl') == msme_rgb['beryl']
    assert extract_palette(msme_rgb['beryl']) == msme_rgb['beryl']
    assert extract_palette(None) is None


def test_make_colormap():
    cmap = make_colormap(['rawdenim', 'lightgray', 'pomegranate'])
    assert isinstance(cmap, Colormap)


def test_msme_colors():
    @msme_colors
    def plot_foo(color='beryl'):
        return color

    def plot_bar(color='beryl'):
        return color

    assert plot_foo() == msme_rgb['beryl']
    assert msme_colors(plot_bar)() == msme_rgb['beryl']
