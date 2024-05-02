import seaborn as sns
import matplotlib.pyplot as plt

def create_seaborn_plots(plot_configs, subplot_titles, nrows, ncols, plot_func, file_path, 
                         answer_key=None, key=None, style='whitegrid', overall_title=None, 
                         x_label=None, y_label=None, secondary_y=False, secondary_y_label=None,
                         log_scale_x=False, log_scale_y=False, three_d=False, z_label=None, show=False, loc='upper left', marker=None, markersize=None, ncols_wanted=1):
    """
    Creates and saves Seaborn plots with flexibility for single or multiple subplots,
    with optional logarithmic scaling on x and/or y axes.

    Args:
        plot_configs (list of list of dict): Configuration for each line in each plot.
        subplot_titles (list of str): Titles for each subplot.
        nrows, ncols (int): Number of rows and columns in the subplot grid.
        plot_func (function): Seaborn plotting function (e.g., sns.lineplot).
        file_path (str): Path where the plot image will be saved.
        answer_key (dict, optional): Dictionary to store the file path. Defaults to None.
        key (str, optional): Key under which the file path will be stored. Defaults to None.
        style (str, optional): Seaborn style. Defaults to 'whitegrid'.
        overall_title (str, optional): Title for the plot grid. Defaults to None.
        x_label (list or str, optional): Label for the x-axis. Defaults to None.
        y_label (list or str, optional): Label for the primary y-axis. Defaults to None.
        secondary_y (list or bool, optional): Whether to include a secondary y-axis. Defaults to False.
        secondary_y_label (str, optional): Label for the secondary y-axis. Defaults to None.
        log_scale_x (list or bool, optional): Whether to use logarithmic scaling on the x-axis. Defaults to False.
        log_scale_y (list or bool, optional): Whether to use logarithmic scaling on the y-axis. Defaults to False.
        three_d (bool, optional): Whether to include a 3D plot. Defaults to False.
        z_label (str, optional): Label for the z-axis in the 3D plot. Defaults to None.
        show (bool, optional): Show plot or not. Defaults to False.
        loc (list or str, optional): Legend location. Defaults to 'upper left'.
        marker (str, optional): Marker type. Defaults to None.
        markersize (int, optional): Size of the markers. Defaults to None.
        ncols_wanted (list or int, optional): Number of legend columns. Defaults to 1.
    """
    sns.set_style(style)
    fig = plt.figure(figsize=(10 * ncols, 5 * nrows))

    if three_d:
        from mpl_toolkits.mplot3d import Axes3D

    for i, (plot_config_row, subplot_title) in enumerate(zip(plot_configs, subplot_titles)):
        ax = fig.add_subplot(nrows, ncols, i + 1, projection='3d' if three_d else None)
        sec_y = secondary_y[i] if isinstance(secondary_y, list) else secondary_y
        sec_y_label = secondary_y_label[i] if isinstance(secondary_y_label, list) else secondary_y_label

        if sec_y:
            secondary_ax = ax.twinx()
            secondary_ax.set_ylabel(sec_y_label)
            if log_scale_y[i] if isinstance(log_scale_y, list) else log_scale_y:
                secondary_ax.set_yscale('log')
        else:
            secondary_ax = None
            if log_scale_y[i] if isinstance(log_scale_y, list) else log_scale_y:
                ax.set_yscale('log')

        if log_scale_x[i] if isinstance(log_scale_x, list) else log_scale_x:
            ax.set_xscale('log')

        for config in plot_config_row:
            data = config['data']
            x_col = config['x_col']
            y_col = config['y_col']
            color = config.get('color', None)
            use_secondary = config.get('use_secondary', False)
            label = config.get('label', None)

            if use_secondary and secondary_ax is not None:
                plot_func(data=data, x=x_col, y=y_col, ax=secondary_ax, color=color, label=label)
            elif three_d:
                ax.plot_trisurf(data[x_col], data[y_col], data[z_label], color=color, label=label)
            else:
                plot_func(data=data, x=x_col, y=y_col, ax=ax, color=color, label=label, marker=marker, markersize=markersize)

        ax.set_title(subplot_title)
        ax.set_xlabel(x_label if isinstance(x_label, list) else x_label)
        ax.set_ylabel(y_label if isinstance(y_label, list) else y_label)
        if three_d:
            ax.set_zlabel(z_label)

        # Manage legend display
        if secondary_ax:
            handles_secondary, labels_secondary = secondary_ax.get_legend_handles_labels()
            secondary_ax.legend(handles_secondary, labels_secondary, loc='upper right')

        handles_primary, labels_primary = ax.get_legend_handles_labels()
        ax.legend(handles_primary, labels_primary, loc=loc if isinstance(loc, list) else loc, ncols=ncols_wanted if isinstance(ncols_wanted, list) else ncols_wanted)

    if overall_title:
        plt.suptitle(overall_title)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(file_path)
    if answer_key is not None and key is not None:
        answer_key[key] = [file_path]
    if show:
        plt.show()
