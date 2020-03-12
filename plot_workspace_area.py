import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def uni_plotter(area_points, border_points, L2, title):
    """
    Plotting the set of inside and border boxes
    :param area_points: area boxes set
    :param border_points: border boxes set
    :param L2: the size of boundary box
    :param title: the name of the method
    """
    left_border = -L2  # Left border of rectangle which we use to build uniform grid
    right_border = L2
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
