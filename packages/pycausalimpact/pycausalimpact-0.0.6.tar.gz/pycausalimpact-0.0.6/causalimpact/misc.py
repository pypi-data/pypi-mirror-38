# MIT License
#
# Copyright (c) 2018 Dafiti OpenSource
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Miscellaneous functions to help in the implementation of Causal Impact."""

import numpy as np
import scipy.stats as stats
from statsmodels.tsa.statespace.structural import UnobservedComponents


def standardize(data):
    """
    Applies standardization to input data. Result should have mean zero and standard
    deviation of one.

    Args
    ----
      data: pandas DataFrame.

    Returns
    -------
      list:
        data: standardized data with zero mean and std of one.
        tuple:
          mean and standard deviation used on each column of input data to make
          standardization. These values should be used to obtain the original dataframe.

    Raises
    ------
      ValueError: if data has only one value.
    """
    if data.shape[0] == 1:
        raise ValueError('Input data must have more than one value')
    mu = data.mean(skipna=True)
    std = data.std(skipna=True, ddof=0)
    data = (data - mu) / std.fillna(1)
    return [data, (mu, std)]


def unstandardize(data, mus_sigs):
    """
    Applies the inverse transformation to return to original data.

    Args
    ----
      data: pandas DataFrame with zero mean and std of one.
      mus_sigs: tuple where first value is the mean used for the standardization and
                second value is the respective standard deviaion.

    Returns
    -------
      data: pandas DataFrame with mean and std given by input ``mus_sigs``
    """
    mu, sig = mus_sigs
    data = (data * sig) + mu
    return data


def get_z_score(p):
    """
    Returns the correspondent z-score with probability area p.

    Args
    ----
      p: float ranging between 0 and 1 representing the probability area to convert.

    Returns
    -------
      The z-score correspondent of p.
    """
    return stats.norm.ppf(p)


def get_referenced_model(model, endog, exog):
    """
    Buils an `UnobservedComponents` model using as reference the input `model`. This is
    mainly used for building models to make simulations of time series.

    Args
    ----
      model: `UnobservedComponents`.
          Template model that is used as reference to build a new one with new `endog`
          and `exog` variables.
      endog: pandas.Series.
          New endog value to be used in model.
      exog: pandas.Series.
          New exog value to be used in model.

    Returns
    -------
      ref_model: `UnobservedComponents`.
          New model built from input `model` setup.
    """
    args = {}
    args['level'] = model.level
    args['trend'] = model.trend
    args['seasonal'] = model.seasonal_periods
    args['freq_seasonal'] = [{'period': period, 'harmonics': h} for (period, h) in zip(
        model.freq_seasonal_periods, model.freq_seasonal_harmonics)]
    args['cycle'] = model.cycle
    args['ar'] = model.ar_order
    args['exog'] = exog
    args['endog'] = endog
    args['irregular'] = model.irregular
    args['stochastic_level'] = model.stochastic_level
    args['stochastic_trend'] = model.stochastic_trend
    args['stochastic_seasonal'] = model.stochastic_seasonal
    args['stochastic_freq_seasonal'] = model.stochastic_freq_seasonal
    args['stochastic_cycle'] = model.stochastic_cycle
    args['damped_cycle'] = model.damped_cycle
    cycle_bounds = model.cycle_frequency_bound
    lower_cycle_bound = 2 * np.pi / cycle_bounds[1]
    upper_cycle_bound = 2 * np.pi / cycle_bounds[0] if cycle_bounds[0] > 0 else np.inf
    args['cycle_period_bounds'] = (lower_cycle_bound, upper_cycle_bound)
    ref_model = UnobservedComponents(**args)
    return ref_model
