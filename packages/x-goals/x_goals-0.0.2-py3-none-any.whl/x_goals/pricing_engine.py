from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from x_goals.state import SingleParamState, ParamStates

"""
Note there is a requirement that the function names agree with the
attribs names as used in state and in weights_params
"""

weights_params = {'corners': 0.15, 'shotson': 0.2, 'cards': -0.1}


def corners_model(param_state: SingleParamState, size: int = 1):
    """
    Given the expected number of corners and the standard deviation
    produce values from the normal distribution

    Parameters
    ----------
    param_state: object of type SingleParamState
    size      int   describing the number of random variables to produce

    Returns
    -------
    list of length size of random realisations of the distribution
    """
    values = param_state.mean + stats.norm.rvs(size=size)*param_state.stdev
    values[values < 0] = param_state.mean + stats.norm.rvs(size=len(values[values < 0]))*param_state.stdev
    return values


def shotson_model(param_state: SingleParamState, size: int = 1):
    """
    Given the expected number of shots on target and the standard deviation
    produce values from the normal distribution

    Parameters
    ----------
    param_state: object of type SingleParamState
    size      int   describing the number of random variables to produce

    Returns
    -------
    list of length size of random realisations of the distribution
    """
    values = param_state.mean + stats.norm.rvs(size=size)*param_state.stdev
    values[values < 0] = param_state.mean + stats.norm.rvs(size=len(values[values < 0]))*param_state.stdev
    return values


def cards_model(param_state: SingleParamState, size: int = 1):
    """
    Given the expected number of cards produce values from the Poisson distribution

    Card has value 1 unit for a yellow card.
    A second yellow or a red for any particular player counts as 2.5 units
    """
    return stats.poisson(param_state.mean).rvs(size=size)


def attrib_distplot(attrib, param_state: SingleParamState):
    if attrib == 'cards':
        kde_show = False
    else:
        kde_show = True

    fig, ax1 = plt.subplots(1, 1)
    sns.distplot(eval(attrib + '_model')(param_state, 10000), norm_hist=True, hist=True,
                 kde=kde_show, kde_kws={'linewidth': 3}, label=attrib, ax=ax1)
    ax1.set(xlabel=attrib, ylabel='probability density')
    return fig


def price_match_V1(param_states_home: ParamStates, param_states_away: ParamStates,
                   niters: int = 10000, approx_stdev: bool = True):
    """
    Using the Poisson model for the cards, and normal distribution for
    shots-on and corners, this routine prices up the odds in a 1x2 format.

    niters number of simulations are used to predict the outcome, by extracting
    the XGoals score on each iteration and averaging the number of outcomes (W-D-L)
    to establish the probability.

    Parameters
    ----------
    param_states_home: parameter values required for the models for the home team
    away_vars_params: as above but for the away team
    niters: int describing number of iterations used in finding the score
    approx_stdev: boolean which when true the standard deviation is approximated by half of the mean

    Returns
    -------
    1x2 probabilities for (home, draw, away)
    """
    results_home = np.zeros(niters)
    results_away = np.zeros(niters)

    attribs = weights_params.keys()
    if approx_stdev:
        for attrib in attribs:
            param_states_home.use_version_one_approx(attrib)
            param_states_away.use_version_one_approx(attrib)

    for attrib in attribs:
        results_home += weights_params[attrib] * eval(attrib + '_model')(getattr(param_states_home, attrib),
                                                                         niters)
        results_away += weights_params[attrib] * eval(attrib + '_model')(getattr(param_states_away, attrib),
                                                                         niters)
    results_home = np.round(results_home, 1)
    results_away = np.round(results_away, 1)

    return (sum(results_home > results_away) / niters, sum(results_home == results_away) / niters,
            sum(results_home < results_away) / niters)
