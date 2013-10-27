
from colormath.color_objects import LCHuvColor
import numpy as np
from matplotlib.colors import Colormap


class MplLCHColor(object):
    # FIXME use slots?

    def __init__(self, luminance, chroma, hue):
        self.__lch_data = (int(luminance), int(chroma), int(hue))
        self.__rgb_data = self.color_object_to_mpl(
            LCHuvColor(luminance, chroma, hue))

    @property
    def lch(self):
        return self.__lch_data

    @property
    def luminance(self):
        return self.__lch_data[0]

    @property
    def chroma(self):
        return self.__lch_data[1]

    @property
    def hue(self):
        return self.__lch_data[2]

    @property
    def rgb(self):
        return self.__rgb_data

    def __len__(self):
        return len(self.__rgb_data)

    def __getitem__(self, key):
        return self.__rgb_data[key]

    def __iter__(self):
        return iter(self.__rgb_data)

    def __repr__(self):
        return "%s<lch=%s, rgb=%s>" % (
            self.__class__.__name__, self.__lch_data,
            tuple(round(c, 3) for c in self.__rgb_data))

    @property
    def tint(self):
        luminance = min(100, 1.5 * self.luminance)
        chroma = max(0, self.chroma / 2.0)
        return MplLCHColor(luminance, chroma, self.hue)

    @property
    def shade(self):
        luminance = max(0, self.luminance / 2.0)
        chroma = 1.5 * self.chroma
        return MplLCHColor(luminance, chroma, self.hue)

    @property
    def radiant(self):
        return MplLCHColor(self.luminance, 255, self.hue)

    @staticmethod
    def color_object_to_mpl(color):
        return tuple(channel / 255.0
                     for channel in color.convert_to('rgb').get_value_tuple())


def create_distinct_colors(
        num, hue_start=0, hue_range=360, luminance=50, chroma=75):
    hues = (hue_start + np.linspace(0, hue_range, num, endpoint=False)) % 360
    return [MplLCHColor(luminance, chroma, hue) for hue in hues]


class Palette(object):
    def __init__(self, base_tones):
        self.by_category = {
            'tones': base_tones,
            'tints': [c.tint for c in base_tones],
            'shades': [c.shade for c in base_tones],
            'radiants': [c.radiant for c in base_tones]
        }
        for category, colors in self.by_category.iteritems():
            setattr(self, category, colors)


class QualitativePalette(object):
    def __init__(
            self, num, hue_start=0, hue_range=360, luminance=50, chroma=75):
        colors = create_distinct_colors(
            num, hue_start, hue_range, luminance, chroma)
        self.by_category = {
            'thick': colors,
            'thin': [c.shade for c in colors],
            'highlight': [c.radiant for c in colors]
        }
        for category, colors in self.by_category.iteritems():
            setattr(self, category, colors)


class SequentialCPalette(Colormap):
    def __init__(self, name, hue, luminance, chroma_range, N=256):
        self.hue = hue
        self.luminance = luminance
        self.chroma_range = chroma_range
        self.monochrome = False
        super(SequentialCPalette, self).__init__(name, N)

    def _init(self):
        chromas = np.linspace(*self.chroma_range, num=self.N)
        self._lut = np.ones((self.N, 4))
        for i, chroma in enumerate(chromas):
            self._lut[i, :3] = MplLCHColor(
                self.luminance, chroma, self.hue).rgb


class SequentialLCPalette(Colormap):
    def __init__(self, name, hue, luminance_range, chroma_range, N=256):
        self.hue = hue
        self.luminance_range = luminance_range
        self.chroma_range = chroma_range
        self.monochrome = False
        super(SequentialLCPalette, self).__init__(name, N)

    def _init(self):
        luminances = np.linspace(*self.luminance_range, num=self.N)
        chromas = np.linspace(*self.chroma_range, num=self.N)
        self._lut = np.ones((self.N, 4))
        for i in xrange(self.N):
            self._lut[i, :3] = MplLCHColor(
                luminances[i], chromas[i], self.hue).rgb
