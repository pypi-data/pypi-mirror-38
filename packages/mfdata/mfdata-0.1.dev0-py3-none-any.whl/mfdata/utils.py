import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from itertools import cycle
from mfdata.dates import *

'''
Plot modules

'''


class plot:

    fed_dates = dates()
    recession_end = fed_dates.recession_end
    last_day = fed_dates.last_day

    def series_plot(self,
                    df,
                    cols,
                    start_date=recession_end,
                    end_date=last_day,
                    sub_figure=True,
                    plot_styles='-',
                    plot_color='black',
                    use_labels=False,
                    labels=None,
                    plottype='series'):

        plt.figure()
        rcParams['font.family'] = 'serif'
        rcParams['font.size'] = 16
        figure_size = (20, 5 * len(cols))

        if type(cols[0]) == str:
            for i in range(len(cols)):
                cols[i] = name2ind(cols[i], df)
        plot_names = [list(df)[i] for i in cols]

        if sub_figure is False:
            figure_size = (20, 6)
        linestyles = ['-', '--', ':', '-.']
        linecycler = cycle(linestyles)

        if sub_figure is False:
            plot_styles = [next(linecycler) for i in cols]
            plot_color = None

        if plottype == 'series':
            df[plot_names][start_date:end_date].plot(subplots=sub_figure,
                                                     figsize=figure_size,
                                                     fontsize=16,
                                                     color=plot_color,
                                                     style=plot_styles,
                                                     grid=True,
                                                     legend=True)
        if plottype == 'area':
            df[plot_names][start_date:end_date].plot.area(subplots=sub_figure,
                                                          figsize=figure_size,
                                                          fontsize=16,
                                                          color=plot_color,
                                                          style=plot_styles,
                                                          grid=True,
                                                          legend=True)

        if use_labels:
            used_labels = [labels[i] for i in cols]
            plt.legend(used_labels, loc='best', fontsize=14)

    def compare_plot(self,
                     df,
                     cols,
                     title=None,
                     start_date=recession_end):
        rcParams['font.family'] = 'serif'
        rcParams['font.size'] = 16
        plt.figure()
        ax = df[cols][start_date:].plot(figsize=(20, 7),
                                        secondary_y=cols[-1],
                                        fontsize=16,
                                        style=['-', '--'],
                                        color=['black', 'red'],
                                        grid=True)
        ax.set_title(title, fontsize=20)


'''
Helper functions
'''


def _change(x, cols, lag):
    diff = x[cols] - x[cols].shift(periods=lag, axis='index')
    rate = diff.iloc[1:] / [cols].shift(periods=lag, axis='index').iloc[1:] - 1
    return diff.iloc[1:], rate * 100


def normalize(x):
    return (x - x.mean(axis=0)) / x.std(axis=0)


def name2ind(text, df):
    for i, item in enumerate(list(df)):
        if item == text:
            return i


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
