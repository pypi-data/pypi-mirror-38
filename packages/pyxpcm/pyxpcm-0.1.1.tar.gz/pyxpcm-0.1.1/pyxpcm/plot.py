#!/bin/env python
# -*coding: UTF-8 -*-
#
# Provide some basic methods for plotting
#
# Created by gmaze on 2017/12/11
__author__ = 'gmaze@ifremer.fr'

# import os
# import sys
# import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors

def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet.
        N: number of colors.
    """
    # source: https://stackoverflow.com/questions/18704353/correcting-matplotlib-colorbar-ticks
    if type(cmap) == str:
        cmap = plt.get_cmap(cmap)
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki])
                      for i in xrange(N + 1)]
    # Return colormap object.
    return mcolors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, N)

class _PlotMethods(object):
    """
    Enables use of pcmpack.plot functions as attributes on a PCM object.
    For example, m.plot.scaler
    """

    def __init__(self, m):
        self._pcm = m

    def __call__(self, **kwargs):
        return plot(self._pcm, **kwargs)

def plot(m, ax=None, subplot_kws=None, **kwargs):
    print "This would trigger a plot of the PCM !"

class _PlotScalerMethods(object):
    """
    Enables use of pcmpack.plot functions as attributes on a PCM object.
    For example, m.plot.scaler
    """

    def __init__(self, m):
        self._pcm = m

    def __call__(self, **kwargs):
        return plot_scaler(self._pcm, **kwargs)

    # @functools.wraps(hist)
    # def hist(self, ax=None, **kwargs):
    #     return hist(self._da, ax=ax, **kwargs)
    #
    # @functools.wraps(line)
    # def line(self, *args, **kwargs):
    #     return line(self._da, *args, **kwargs)

def scaler(m, ax=None, subplot_kws=None, **kwargs):
    X_ave = m._scaler.mean_
    X_std = m._scaler.scale_
    X_unit = m._scaler_props['units']
    feature_axis = m._props['feature_axis']
    feature_name = m._props['feature_name']
    print X_ave
    print feature_axis

    fig, ax = plt.subplots(nrows=1, ncols=2, sharey='row', figsize=(10, 5), dpi=80, facecolor='w', edgecolor='k')
    ax[0].plot(X_ave, feature_axis, '-', linewidth=2, label='Sample Mean')
    ax[1].plot(X_std, feature_axis, '-', linewidth=2, label='Sample Std')
    # tidy up the figure
    ax[0].set_ylabel('Feature axis')
    for ix in range(0, 2):
        ax[ix].legend(loc='lower right')
        ax[ix].grid(True)
        ax[ix].set_xlabel("[%s]" % X_unit)
    fig.suptitle("Feature: %s" % feature_name, fontsize=12)
    plt.show()

def quant(m, da, xlim=None):
    """Plot the q-th quantiles of a dataArray for each PCM component

        Parameters
        ----------
        m: PCM class instance
        da: xarray.DataArray with quantiles

        Returns
        -------
        -

    """
    cmap = cmap_discretize(plt.cm.Paired, m.K)
    # da must 3D with a dimension for: CLASS, QUANTILES and a vertical axis
    # The QUANTILES dimension is called "quantile"
    # The CLASS dimension is identified as the one matching m.K length.
    if (np.argwhere(np.array(da.shape) == m.K).shape[0]>1):
        raise ValueError("Can't distinguish the class dimension from the others")
    for (i, iname) in zip(da.shape, da.dims):
        if i == m.K:
            CLASS_DIM = iname
        elif iname == 'quantile':
            QUANT_DIM = 'quantile'
        else:
            VERTICAL_DIM = iname

    fig, ax = plt.subplots(nrows=1, ncols=m.K, figsize=(2 * m.K, 4), dpi=80, facecolor='w', edgecolor='k', sharey='row')
    if not xlim:
        xlim = np.array([0.9 * da.min(), 1.1 * da.max()])
    for k in range(m.K):
        Qk = da.sel(N_CLASS=k)
        for q in Qk['quantile']:
            Qkq = Qk.sel(quantile=q)
            ax[k].plot(Qkq.values.T, da[VERTICAL_DIM], label=("%0.2f") % (Qkq['quantile']), color=cmap(k))
        ax[k].set_title(("Component: %i") % (k), color=cmap(k))
        ax[k].legend(loc='lower right')
        ax[k].set_xlim(xlim)
        ax[k].set_ylim(np.array([da[VERTICAL_DIM].min(), da[VERTICAL_DIM].max()]))
        # ax[k].set_xlabel(Q.units)
        if k == 0: ax[k].set_ylabel('feature dimension')
        ax[k].grid(True)
    plt.tight_layout()

