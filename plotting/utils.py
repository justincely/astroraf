
__all__ = ['init_plots','format_axis','big_ticks']

def init_plots(figsize=(20,8.5)):
    """
    Sets plotting defaults to make things pretty
    
    """

    try: matplotlib
    except NameError: import matplotlib

    matplotlib.rcParams['lines.markeredgewidth'] = .001
    matplotlib.rcParams['lines.linewidth']=2
    matplotlib.rcParams['patch.edgecolor']='grey'
    matplotlib.rcParams['font.size']=15.0
    matplotlib.rcParams['figure.figsize']=figsize
    matplotlib.rcParams['figure.subplot.left']=.1
    matplotlib.rcParams['figure.subplot.right']=.9
    matplotlib.rcParams['figure.subplot.top']=.92
    matplotlib.rcParams['figure.subplot.bottom']=.1
    matplotlib.rcParams['figure.subplot.wspace']=.2
    matplotlib.rcParams['figure.subplot.hspace']=.2
    matplotlib.rcParams['figure.facecolor']='white'
    matplotlib.rcParams['axes.facecolor']='white'
    matplotlib.rcParams['axes.edgecolor']='black'
    matplotlib.rcParams['axes.linewidth']=1
    matplotlib.rcParams['axes.grid']=True
    matplotlib.rcParams['xtick.major.size']=7
    matplotlib.rcParams['ytick.major.size']=7
    matplotlib.rcParams['xtick.minor.size']=4
    matplotlib.rcParams['ytick.minor.size']=4


def format_axis(precision='%.1f',ticksize=1,axis=None,which='both'):
    """
    from matplotlib.ticker import *
    formats axis label precision

    """

    import matplotlib.pyplot as plt
    from matplotlib.ticker import FormatStrFormatter

    if not axis:
        axis = plt.gca()

    if which in ('x','X','both'): axis.xaxis.set_major_formatter(FormatStrFormatter(precision))
    if which in ('y','Y','both'): axis.yaxis.set_major_formatter(FormatStrFormatter(precision))


def big_ticks(width=1,axis=None):
    """
    #for each axis or whichever axis you want you should
    Increases major tick size

    """

    import matplotlib.pyplot as plt

    if not axis:
        axis = plt.gca()
    for line in axis.xaxis.get_ticklines(): line.set_markeredgewidth(width)
    for line in axis.yaxis.get_ticklines(): line.set_markeredgewidth(width)
