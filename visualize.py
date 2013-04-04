import matplotlib.pyplot as plt


def plot_colors(colors, (x, y)=0, (width, height)=(1, 1), axes=None):
    if axes is None:
        axes = plt.gca()
    for i, color in enumerate(colors):
        axes.add_patch(plt.Rectangle(
            (x + i * width, y), width, height, color=color))


def plot_palette(palette, fig=None):
    if fig is None:
        fig = plt.figure()
    axes = fig.add_axes([0, 0, 1, 1])
    axes.set_ylim(0, len(palette.by_category))
    axes.set_aspect('equal')
    axes.set_axis_off()
    xlim = 1
    for i, colors in enumerate(palette.by_category.itervalues()):
        xlim = max(xlim, len(colors))
        plot_colors(colors, (0, i), axes=axes)
    axes.set_xlim(0, xlim)


#def create_example_plot(colors):
    #x = np.linspace(0, 3 * np.pi, 100)
    #fig = plt.figure()
    #axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    #for i, color in enumerate(colors):
        #axes.plot(
            #x, np.sin(x + 2 * np.pi * i / len(colors)),
            #linewidth=3)


#def create_example_scatter_plot(colors):
    #from numpy.random import multivariate_normal
    #covs = [np.array([[4.0, 0.0], [0.0, 0.1]]),
            #np.array([[5.0, 2.0], [2.0, 1.0]]),
            #np.array([[0.5, 0.0], [0.0, 5.0]])]
    #data = [multivariate_normal((0, 0), cov, 50) for cov in covs]

    #fig = plt.figure()
    #axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    #axes.set_aspect('equal')
    #for item, color in zip(data, colors):
        #axes.scatter(item[:, 0], item[:, 1])
