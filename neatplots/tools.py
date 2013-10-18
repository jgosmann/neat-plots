import itertools

from matplotlib.artist import allow_rasterization, Artist
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec, SubplotSpec
from matplotlib.transforms import Bbox
from matplotlib import text


# FIXME test this class
class Broadcast(list):
    def __getattr__(self, name):
        return self.broadcast(name)

    def __setattr__(self, name, value):
        for obj in self:
            setattr(obj, name, value)

    def __delattr__(self, name):
        for obj in self:
            delattr(obj, name)

    def __call__(self, *args, **kwargs):
        return Broadcast([f(*args, **kwargs) for f in self])

    def broadcast(self, name):
        return Broadcast(getattr(obj, name) for obj in self)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__, super(Broadcast, self).__repr__())


class JoinedYAxesLabel(Artist):
    def __init__(self, yaxes, labeltext, fontdict=None, **kwargs):
        super(JoinedYAxesLabel, self).__init__()
        self.yaxes = Broadcast(yaxes)
        self.label = text.Text(
            0, 0, labeltext, rotation_mode='anchor', rotation='vertical',
            horizontalalignment='center', verticalalignment='bottom')
        if fontdict is not None:
            self.label.update(fontdict)
        self.label.update(kwargs)
        self.labelpad = 5

    def get_window_extent(self, renderer):
        return self.label.get_window_extent(renderer)

    def get_children(self):
        return [self.label]

    def set_figure(self, fig):
        super(JoinedYAxesLabel, self).set_figure(fig)
        self.label.set_figure(fig)

    @allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        bbox = Bbox.union(self.yaxes.get_ticklabel_extents(
            renderer).broadcast('__getitem__')(0))
        x = bbox.xmin - self.labelpad * self.get_figure().dpi / 72.0
        y = (bbox.ymin + bbox.ymax) / 2.0
        self.label.set_position((x, y))
        self.label.draw(renderer, *args, **kwargs)


# FIXME can this be tested?
class HSplitAxes(object):
    def __init__(
            self, figure, subplot_spec=SubplotSpec(GridSpec(1, 1), 0),
            ratio=0.5, spacing=0.1, sharex=None, sharey=(None, None)):
        self.figure = figure
        self.grid = GridSpecFromSubplotSpec(
            2, 1, subplot_spec, height_ratios=(ratio, 1.0 - ratio),
            hspace=spacing)

        if sharey is None:
            sharey = (None, None)

        self.top = figure.add_subplot(
            self.grid[0], sharex=sharex, sharey=sharey[0])
        if sharex is None:
            sharex = self.top
        self.bottom = figure.add_subplot(
            self.grid[1], sharex=sharex, sharey=sharey[1])
        self.both = Broadcast([self.top, self.bottom])

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

    def set_xlabel(self, xlabel, fontdict=None, labelpad=None, **kwargs):
        self.bottom.set_xlabel(xlabel, fontdict, labelpad, **kwargs)

    def set_ylabel(self, ylabel, fontdict=None, labelpad=None, **kwargs):
        a = JoinedYAxesLabel(self.both.yaxis, ylabel, fontdict, **kwargs)
        if labelpad is not None:
            a.labelpad = labelpad
        a.set_figure(self.figure)
        self.figure.texts.append(a)

    def set_title(self, label, fontdict=None, loc="center", **kwargs):
        self.top.set_title(label, fontdict, loc, **kwargs)


class SharedAxesGrid(object):
    def __init__(self, rows_data, cols_data):
        grid = GridSpec(len(rows_data), len(cols_data))
        self.axes_by_row = []
        self.axes_by_col = []
        self.axes = Broadcast()
        for i, ((row, row_data), (col, col_data)) in enumerate(
                itertools.product(enumerate(rows_data), enumerate(cols_data))):
            if row <= 0:
                sharex = None
            if col <= 0:
                sharey = None

            ax = self._create_axes(grid[i], sharex, sharey)

            x, y = self._get_share_xy(ax)
            if row <= 0:
                sharex = x
                self.axes_by_col.append(Broadcast([ax]))
            else:
                self.axes_by_col[-1].append(ax)
            if col <= 0:
                sharey = y
                self.axes_by_row.append(Broadcast([ax]))
            else:
                self.axes_by_row[-1].append(ax)
            self.axes.append(ax)

            self._plot(ax, row_data, col_data)

    def _create_axes(self, subplot_spec, sharex, sharey):
        raise NotImplementedError()

    def _get_share_xy(self, axes):
        return axes, axes

    def _plot(self, axes, row_data, col_data):
        pass
