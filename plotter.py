import seaborn as sns
import matplotlib.pyplot as plt

def initialize_style(style, overall_title, figsize):
    """Set the aesthetic style of the plots.

    Args:
        style (str): The aesthetic style of the plots (e.g., 'whitegrid').
        overall_title (str): Title for the entire figure.
        figsize (tuple): Dimension tuple for the figure size, e.g., (width, height).
    Returns:
        matplotlib.figure.Figure: The figure object initialized with the style and size.
    """
    sns.set_style(style)
    fig = plt.figure(figsize=figsize)
    if overall_title:
        plt.suptitle(overall_title)
    return fig

def add_subplot(fig, nrows, ncols, index, projection=None):
    """Add a subplot to the figure.

    Args:
        fig (matplotlib.figure.Figure): The main figure object.
        nrows (int): Number of rows in the subplot grid.
        ncols (int): Number of columns in the subplot grid.
        index (int): Index of the subplot in the grid.
        projection (str): The projection type of the subplot (e.g., '3d').

    Returns:
        matplotlib.axes.Axes: The axes object of the subplot.
    """
    return fig.add_subplot(nrows, ncols, index, projection=projection)

def configure_axes(ax, config, is_secondary=False):
    """Configure axes settings for a subplot.

    Args:
        ax (matplotlib.axes.Axes): Axes object to configure.
        config (dict): Configuration for axes settings.
        is_secondary (bool): Flag to configure as a secondary axis.

    """
    if is_secondary:
        ax.set_ylabel(config['label'])
        if config['log_scale']:
            ax.set_yscale('log')
    else:
        ax.set_xlabel(config['x_label'])
        ax.set_ylabel(config['y_label'])
        ax.set_title(config['title'])
        if config['log_scale']:
            ax.set_yscale('log')
        if config['log_scale_x']:
            ax.set_xscale('log')

def plot_data(ax, plot_func, config, use_secondary=False, secondary_ax=None):
    """Plot data on the given axes.

    Args:
        ax (matplotlib.axes.Axes): Primary axes object for plotting.
        plot_func (callable): The seaborn plotting function to use.
        config (dict): Plot configuration including data and aesthetic settings.
        use_secondary (bool): Whether to plot on the secondary axis.
        secondary_ax (matplotlib.axes.Axes): Secondary axes object for plotting.

    """
    if use_secondary and secondary_ax:
        target_ax = secondary_ax
    else:
        target_ax = ax

    plot_func(data=config['data'], x=config['x_col'], y=config['y_col'], ax=target_ax, 
              color=config.get('color'), label=config.get('label'), 
              marker=config.get('marker'), markersize=config.get('markersize'))

def finalize_plot(fig, file_path, show):
    """Finalize the plot by adjusting layout, saving, and showing the plot.

    Args:
        fig (matplotlib.figure.Figure): The figure object containing all subplots.
        file_path (str): Path to save the figure.
        show (bool): Whether to display the plot.
    """
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(file_path)
    if show:
        plt.show()
    plt.close(fig)

def create_seaborn_plots(plot_configs, subplot_titles, nrows, ncols, plot_func, file_path, 
                         style='whitegrid', overall_title=None, figsize=(15, 10), show=False):
    """Creates a grid of seaborn plots based on detailed configuration settings.

    Args:
        plot_configs (list of dict): Configuration for each subplot including data and aesthetics.
        subplot_titles (list of str): Titles for each subplot.
        nrows (int): Number of rows in the subplot grid.
        ncols (int): Number of columns in the subplot grid.
        plot_func (function): Seaborn plotting function to use, such as sns.lineplot.
        file_path (str): File path where the plot image will be saved.
        style (str): Seaborn style for the plots. Defaults to 'whitegrid'.
        overall_title (str): Overall title for the plot grid.
        figsize (tuple): Tuple specifying the figure size.
        show (bool): If True, display the plot after creation.

    """
    fig = initialize_style(style, overall_title, figsize)
    for i, (config, title) in enumerate(zip(plot_configs, subplot_titles)):
        ax = add_subplot(fig, nrows, ncols, i + 1)
        configure_axes(ax, {
            'x_label': config.get('x_label'), 'y_label': config.get('y_label'), 
            'title': title, 'log_scale': config.get('log_scale', False), 
            'log_scale_x': config.get('log_scale_x', False)
        })
        if config.get('secondary_y'):
            secondary_ax = ax.twinx()
            configure_axes(secondary_ax, {'label': config.get('secondary_y_label'), 'log_scale': config.get('log_scale_y', False)}, is_secondary=True)
            plot_data(ax, plot_func, config, use_secondary=True, secondary_ax=secondary_ax)
        plot_data(ax, plot_func, config)
    finalize_plot(fig, file_path, show)
