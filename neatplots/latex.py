import matplotlib


class LatexBeamer(object):
    aspect_ratios = {
        '16:10': (160, 100),
        '16:9': (160, 90),
        '14:9': (140, 90),
        '5:4': (125, 100),
        '4:3': (128, 96),
        '3:2': (135, 90)
    }

    def __init__(self):
        self.font_size = 11
        self.frame_size = self.aspect_ratios['4:3']
        self.margins = (10, 10, 10, 20)

    def __getattr__(self, name):
        with_setter_prefix = 'with_'
        if name.startswith(with_setter_prefix):
            attribute_name = name[len(with_setter_prefix):]
            if not hasattr(self, attribute_name):
                raise AttributeError(name)

            def __with_setter(value):
                setattr(self, attribute_name, value)
                return self
            return __with_setter
        raise AttributeError(name)

    def with_aspect_ratio(self, ratio):
        return self.with_frame_size(self.aspect_ratios[ratio])

    def apply(self):
        scaling = 0.1 / 2.54
        width = self.frame_size[0] - sum(self.margins[:2])
        height = self.frame_size[1] - sum(self.margins[2:])
        figsize = (scaling * width, scaling * height)
        matplotlib.rcParams.update({
            'font.size': self.font_size,
            'figure.figsize': figsize
        })
