
from colormath.color_objects import LCHuvColor
import matplotlib.pyplot as plt
import numpy as np


def to_mpl_color(color):
    return tuple(channel / 255.0
                 for channel in color.convert_to('rgb').get_value_tuple())


def create_distinct_colors(
        num, hue_start=0, hue_range=360, luminance=50, chroma=75):
    hues = (hue_start + np.linspace(0, hue_range, num, endpoint=False)) % 360
    return [LCHuvColor(luminance, chroma, hue) for hue in hues]


def tint_of(color):
    lch = color.convert_to('lchuv')
    luminance = min(100, 1.5 * lch.lch_l)
    chroma = max(0, lch.lch_c / 2.0)
    return LCHuvColor(luminance, chroma, lch.lch_h)


def shade_of(color):
    lch = color.convert_to('lchuv')
    luminance = max(0, lch.lch_l / 2.0)
    chroma = 1.5 * lch.lch_c
    return LCHuvColor(luminance, chroma, lch.lch_h)


def hue_of(color):
    lch = color.convert_to('lchuv')
    return LCHuvColor(lch.lch_l, 255, lch.lch_h)


def plot_palette(palette):
    fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    axes.set_xlim(0, len(palette))
    axes.set_ylim(0, 4)
    axes.set_aspect('equal')
    axes.set_axis_off()
    for i, color in enumerate(palette.tones):
        axes.add_patch(plt.Rectangle((i, 0), 1, 1, color=to_mpl_color(color)))
    for i, color in enumerate(palette.tints):
        axes.add_patch(plt.Rectangle((i, 1), 1, 1, color=to_mpl_color(color)))
    for i, color in enumerate(palette.shades):
        axes.add_patch(plt.Rectangle((i, 2), 1, 1, color=to_mpl_color(color)))
    for i, color in enumerate(palette.hues):
        axes.add_patch(plt.Rectangle((i, 3), 1, 1, color=to_mpl_color(color)))


class Palette(object):
    def __init__(self, base_tones):
        self.tones = base_tones
        self.tints = [tint_of(c) for c in base_tones]
        self.shades = [shade_of(c) for c in base_tones]
        self.hues = [hue_of(c) for c in base_tones]

    def __len__(self):
        return len(self.tones)


def create_example_plot(colors):
    x = np.linspace(0, 3 * np.pi, 100)
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    for i, color in enumerate(colors):
        axes.plot(
            x, np.sin(x + 2 * np.pi * i / len(colors)),
            linewidth=3)


def create_example_scatter_plot(colors):
    from numpy.random import multivariate_normal
    covs = [np.array([[4.0, 0.0], [0.0, 0.1]]),
            np.array([[5.0, 2.0], [2.0, 1.0]]),
            np.array([[0.5, 0.0], [0.0, 5.0]])]
    data = [multivariate_normal((0, 0), cov, 50) for cov in covs]

    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_aspect('equal')
    for item, color in zip(data, colors):
        axes.scatter(item[:, 0], item[:, 1])
