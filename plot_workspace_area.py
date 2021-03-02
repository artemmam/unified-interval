import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib import colors

def plot_circles(r1, r2, d, ax):
    circle = plt.Circle((-0.5*d, 0), radius=r1, fc='y', fill=False)
    ax.add_patch(circle)
    circle = plt.Circle((0.5*d, 0), radius=r1, fc='y', fill=False)
    ax.add_patch(circle)
    circle = plt.Circle((-0.5*d, 0), radius=r2, fc='y', fill=False)
    ax.add_patch(circle)
    circle = plt.Circle((0.5*d, 0), radius=r2, fc='y', fill=False)
    ax.add_patch(circle)

def onclick(event):
    global ix, iy
    ix = event.xdata
    iy = event.ydata
    gl_logger.find_box(ix, iy)

def uni_plotter(area_points, border_points, L2, title, logger = 0, ax = 0):
    """
    Plotting the set of inside and border boxes
    :param area_points: area boxes set
    :param border_points: border boxes set
    :param L2: the size of boundary box
    :param title: the name of the method
    """
    global gl_logger
    gl_logger = logger
    plt.rcParams.update({'font.size': 18})
    left_border = -L2  # Left border of rectangle which we use to build uniform grid
    right_border = L2
    if ax == 0:
        fig, ax = plt.subplots(figsize=(8, 8))
    x_min, y_min, x_max, y_max = left_border - 1, left_border - 1, right_border + 1, right_border + 1
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    rect1 = Rectangle([left_border, left_border], 2*right_border, 2*right_border, fill=False, color='g',
                      linewidth=2.0)
    ax.add_patch(rect1)
    ax.axes.set_aspect('equal')
    for i in range(len(area_points)):  # Plot rectangles, which compose workspace area
        rect1 = Rectangle([area_points[i][0][0], area_points[i][1][0]],
                          area_points[i][0][1] - area_points[i][0][0],
                          area_points[i][1][1] - area_points[i][1][0],
                          fill=True, fc='green', color='black', linewidth=1.0, alpha=1)
        ax.add_patch(rect1)
    for i in range(len(border_points)):  # Plot rectangles, which compose the border of workspace area
        rect2 = Rectangle([border_points[i][0][0], border_points[i][1][0]],
                          border_points[i][0][1] - border_points[i][0][0],
                          border_points[i][1][1] - border_points[i][1][0],
                          fill=True, fc='yellow', color='black', linewidth=1.0, alpha=1)
        ax.add_patch(rect2)
    ax.set_title(title)
    if logger!=0:
        cid = fig.canvas.mpl_connect('button_press_event', onclick)





def iter_plot(s_all, N):
    s_class = s_all[:N**2].reshape(N, N)
    s_bic = s_all[N**2:].reshape(N, N)
    fig = plt.figure(figsize=(16, 8))

    grid = AxesGrid(fig, 111,
                    nrows_ncols=(1, 2),
                    axes_pad=0.5,
                    cbar_mode='single',
                    cbar_location='right',
                    cbar_pad=0.1
                    )
    ax1 = grid[0].imshow(s_class, cmap = plt.cm.get_cmap('viridis_r', 12), interpolation='none')
    ax2 = grid[1].imshow(s_bic, cmap = plt.cm.get_cmap('viridis_r', 12), interpolation='none')
    grid[0].set_title("Classical")
    grid[1].set_title("Bicentered")
    ax = [ax1, ax2]
    vmin = min(image.get_array().min() for image in ax)
    vmax = max(image.get_array().max() for image in ax)
    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    for im in ax:
        im.set_norm(norm)
    cbar1 = grid.cbar_axes[0].colorbar(ax1)


    plt.show()


def plot_all_methods(methods, points, L2, example, L1v = 0, L2v = 0, d = 0):
    n = len(methods)
    fig, ax = plt.subplots(n, 1, figsize=(4, 12))
    for i, method in enumerate(methods):
        uni_plotter(points[method].area_points, points[method].border_points, L2, method, logger=0, ax=ax[i])
        if example == "2rpr":
            plot_circles(L1v, L2v, d, ax[i])







"""
def iter_plot(s_class, N, title):
    s_class = s_class.reshape(N, N)
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.imshow(s_class, cmap = plt.cm.get_cmap('viridis_r', 10), interpolation='none')
    #plt.pcolor(s_class, cmap=plt.get_cmap('viridis_r', 50))

    plt.colorbar()
    ax.set_title(title + " method")
    """