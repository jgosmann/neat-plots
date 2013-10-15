from matplotlib.gridspec import GridSpecFromSubplotSpec


class HSplitAxes(object):
    def __init__(
            self, figure, subplot_spec=1, ratio=0.5, spacing=0.1,
            sharex=None, sharey_top=None, sharey_bottom=None):
        self.grid = GridSpecFromSubplotSpec(
            2, 1, subplot_spec, height_ratios=(ratio, 1.0 - ratio),
            hspace=spacing)

        self.top = figure.add_subplot(
            self.grid[0], sharex=sharex, sharey=sharey_top)
        if sharex is None:
            sharex = self.top
        self.bottom = figure.add_subplot(
            self.grid[1], sharex=sharex, sharey=sharey_bottom)

        self.__init_spines_and_ticks(self.top, self.bottom)
        self.__draw_tear_marks(self.top, self.bottom, ratio)

    @staticmethod
    def __init_spines_and_ticks(top, bottom):
        top.spines['bottom'].set_visible(False)
        bottom.spines['top'].set_visible(False)
        top.xaxis.tick_top()
        bottom.xaxis.tick_bottom()
        top.tick_params(labeltop='off')

    @staticmethod
    def __draw_tear_marks(top, bottom, ratio, size=0.015):
        kwargs = dict(transform=top.transAxes, color='k', clip_on=False)
        y = (-size, +size)
        top.plot((-size, +size), y, **kwargs)
        top.plot((1 - size, 1 + size), y, **kwargs)

        kwargs.update(transform=bottom.transAxes)
        s = ratio / (1.0 - ratio)
        y = (1 - size * s, 1 + size * s)
        bottom.plot((-size, +size), y, **kwargs)
        bottom.plot((1 - size, 1 + size), y, **kwargs)
