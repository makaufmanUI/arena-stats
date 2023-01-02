import pandas as pd
from matplotlib import pyplot as plt




def plot_rating(df: pd.DataFrame, showEnemy: bool = False):
    fig, ax = plt.subplots()
    fig.tight_layout()
    ratings = df['newTeamRating'].astype(int)
    max_rating = max(ratings)
    ax.plot(ratings, color='#83c9ff')
    ax.hline(max_rating)
    ax.set_xlabel('Match', fontsize=10, color='#ebebd6', labelpad=15)
    ax.tick_params(axis='x', which='major', labelsize=10, color='#0e1117', labelcolor='#ebebd6', pad=10)
    ax.tick_params(axis='y', which='major', labelsize=10, color='#0e1117', labelcolor='#ebebd6', pad=10)
    if showEnemy:
        ratings = df['enemyNewTeamRating'].astype(int)
        ax.plot(ratings, color='xkcd:light red')
    ax.set_facecolor('#0e1117')
    fig.set_facecolor('#0e1117')
    return fig





def sort_tuple(tup: tuple) -> tuple:
    """
    Sorts the given tuple so that the elements are in alphabetical order.
    """
    tup = sorted(tup, key=str.lower)
    return tup
