import seaborn as sns
import matplotlib.pyplot as plt

def create_seaborn_plots(plot_configs, subplot_titles, nrows, ncols, plot_func, file_path, 
                         answer_key=None, key=None, style='whitegrid', overall_title=None, 
                         three_d=False, show=False, default_marker=None, default_markersize=None, figsize = (10, 5)):
    """
    Creates and saves Seaborn plots with flexibility for single or multiple subplots,
    with optional attributes specified per subplot in the plot configurations.

    Args:
        plot_configs (list of list of dict): Configuration for each line in each subplot, including labels and scaling.
        subplot_titles (list of str): Titles for each subplot.
        nrows, ncols (int): Number of rows and columns in the subplot grid.
        plot_func (function): Seaborn plotting function (e.g., sns.lineplot).
        file_path (str): Path where the plot image will be saved.
        answer_key (dict, optional): Dictionary to store the file path. Defaults to None.
        key (str, optional): Key under which the file path will be stored. Defaults to None.
        style (str, optional): Seaborn style. Defaults to 'whitegrid'.
        overall_title (str, optional): Title for the plot grid. Defaults to None.
        three_d (bool, optional): Whether to include a 3D plot. Defaults to False.
        show (bool, optional): Show plot or not. Defaults to False.
        default_marker (str, optional): Default marker type if not specified per plot. Defaults to None.
        default_markersize (int, optional): Default size of the markers if not specified per plot. Defaults to None.
        figsize (tuple, optional): Figsize. Defaults to (10, 5).
    """
    sns.set_style(style)
    fig = plt.figure(figsize=figsize)

    if three_d:
        from mpl_toolkits.mplot3d import Axes3D

    for i, (plot_config_row, subplot_title) in enumerate(zip(plot_configs, subplot_titles)):
        ax = fig.add_subplot(nrows, ncols, i + 1, projection='3d' if three_d else None)

        # Set up axes with potential custom settings per subplot
        x_label = plot_config_row[0].get('x_label', None)
        y_label = plot_config_row[0].get('y_label', None)
        sec_y = plot_config_row[0].get('secondary_y', False)
        log_scale_x = plot_config_row[0].get('log_scale_x', False)
        log_scale_y = plot_config_row[0].get('log_scale_y', False)
        z_label = plot_config_row[0].get('z_label', None) if three_d else None

        secondary_ax = None
        if sec_y:
            secondary_ax = ax.twinx()
            secondary_ax.set_ylabel(plot_config_row[0].get('secondary_y_label', 'Secondary Y-axis'))

        for config in plot_config_row:
            data = config['data']
            x_col = config['x_col']
            y_col = config['y_col']
            color = config.get('color', None)
            marker = config.get('marker', default_marker)
            markersize = config.get('markersize', default_markersize)
            use_secondary = config.get('use_secondary', False)
            label = config.get('label', None)
            linestyle = config.get('linestyle', None)

            target_ax = secondary_ax if use_secondary else ax
            if target_ax:
                plot_func(data=data, x=x_col, y=y_col, ax=target_ax, color=color, label=label, marker=marker, markersize=markersize, linestyle=linestyle)
                if log_scale_y:
                    target_ax.set_yscale('log')
                if log_scale_x:
                    target_ax.set_xscale('log')

        ax.set_title(subplot_title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if three_d:
            ax.set_zlabel(z_label)

        # Manage legend display
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper left') if label != None else None

        if secondary_ax:
            handles_secondary, labels_secondary = secondary_ax.get_legend_handles_labels()
            secondary_ax.legend(handles_secondary, labels_secondary, loc='upper right')

    if overall_title:
        plt.suptitle(overall_title)

    plt.tight_layout()
    plt.savefig(file_path)
    if answer_key is not None and key is not None:
        answer_key[key] = [file_path]
    if show:
        plt.show()
