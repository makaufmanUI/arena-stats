import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations



def parse_csv(csv: str) -> pd.DataFrame:
    lines = csv.splitlines()
    lines.pop(0)
    headers = lines[0].split(',')
    rows = []
    for line in lines[1:]:
        row = line.split(',')
        row.pop(-1)
        rows.append(row)
    return pd.DataFrame(rows, columns=headers)



def simplify_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.loc[:, (df != '').any(axis=0)]
    df = df.drop(columns=['isRanked', 'startTime', 'endTime', 'zoneId'])
    df = df.drop(columns=['teamPlayerRace1', 'teamPlayerRace2', 'enemyPlayerRace1', 'enemyPlayerRace2'])
    df = df.iloc[10:]
    df = df.copy().reset_index(drop=True)
    df['win'] = df['teamColor'] == df['winnerColor']
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df = df.drop(columns=['teamColor', 'winnerColor'])
    df = df.drop(columns=['teamPlayerName1', 'teamPlayerName2', 'teamPlayerClass1', 'teamPlayerClass2', 'enemyFaction'])
    df = df.drop(columns=['newTeamRating', 'mmr', 'enemyNewTeamRating', 'enemyDiffRating', 'enemyMmr', 'enemyPlayerName1', 'enemyPlayerName2'])
    return df



def plot_rating(df: pd.DataFrame, title: str = 'Rating', showEnemy: bool = False):
    plt.title(title)
    plt.xlabel('Game')
    plt.ylabel('Rating')
    ratings = df['oldTeamRating'].astype(int)
    plt.plot(ratings, label='Team Rating')
    if showEnemy:
        enemyRatings = df['enemyOldTeamRating'].astype(int)
        plt.plot(enemyRatings, label='Enemy Rating')
        plt.legend()
    plt.show()



def calculate_win_rates(df: pd.DataFrame) -> dict:
    wins = df['win'].sum()
    losses = len(df) - wins
    rate = wins / len(df)
    gamesAgainstWarriors = len(df.loc[df['enemyPlayerClass1'] == 'WARRIOR']) + len(df.loc[df['enemyPlayerClass2'] == 'WARRIOR'])
    gamesAgainstPaladins = len(df.loc[df['enemyPlayerClass1'] == 'PALADIN']) + len(df.loc[df['enemyPlayerClass2'] == 'PALADIN'])
    gamesAgainstHunters = len(df.loc[df['enemyPlayerClass1'] == 'HUNTER']) + len(df.loc[df['enemyPlayerClass2'] == 'HUNTER'])
    gamesAgainstRogues = len(df.loc[df['enemyPlayerClass1'] == 'ROGUE']) + len(df.loc[df['enemyPlayerClass2'] == 'ROGUE'])
    gamesAgainstPriests = len(df.loc[df['enemyPlayerClass1'] == 'PRIEST']) + len(df.loc[df['enemyPlayerClass2'] == 'PRIEST'])
    gamesAgainstDeathKnights = len(df.loc[df['enemyPlayerClass1'] == 'DEATHKNIGHT']) + len(df.loc[df['enemyPlayerClass2'] == 'DEATHKNIGHT'])
    gamesAgainstShamans = len(df.loc[df['enemyPlayerClass1'] == 'SHAMAN']) + len(df.loc[df['enemyPlayerClass2'] == 'SHAMAN'])
    gamesAgainstMages = len(df.loc[df['enemyPlayerClass1'] == 'MAGE']) + len(df.loc[df['enemyPlayerClass2'] == 'MAGE'])
    gamesAgainstWarlocks = len(df.loc[df['enemyPlayerClass1'] == 'WARLOCK']) + len(df.loc[df['enemyPlayerClass2'] == 'WARLOCK'])
    gamesAgainstDruids = len(df.loc[df['enemyPlayerClass1'] == 'DRUID']) + len(df.loc[df['enemyPlayerClass2'] == 'DRUID'])
    winsAgainstWarriors = df.loc[df['enemyPlayerClass1'] == 'WARRIOR', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'WARRIOR', 'win'].sum()
    lossesAgainstWarriors = gamesAgainstWarriors - winsAgainstWarriors
    winsAgainstPaladins = df.loc[df['enemyPlayerClass1'] == 'PALADIN', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'PALADIN', 'win'].sum()
    lossesAgainstPaladins = gamesAgainstPaladins - winsAgainstPaladins
    winsAgainstHunters = df.loc[df['enemyPlayerClass1'] == 'HUNTER', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'HUNTER', 'win'].sum()
    lossesAgainstHunters = gamesAgainstHunters - winsAgainstHunters
    winsAgainstRogues = df.loc[df['enemyPlayerClass1'] == 'ROGUE', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'ROGUE', 'win'].sum()
    lossesAgainstRogues = gamesAgainstRogues - winsAgainstRogues
    winsAgainstPriests = df.loc[df['enemyPlayerClass1'] == 'PRIEST', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'PRIEST', 'win'].sum()
    lossesAgainstPriests = gamesAgainstPriests - winsAgainstPriests
    winsAgainstDeathKnights = df.loc[df['enemyPlayerClass1'] == 'DEATHKNIGHT', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'DEATHKNIGHT', 'win'].sum()
    lossesAgainstDeathKnights = gamesAgainstDeathKnights - winsAgainstDeathKnights
    winsAgainstShamans = df.loc[df['enemyPlayerClass1'] == 'SHAMAN', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'SHAMAN', 'win'].sum()
    lossesAgainstShamans = gamesAgainstShamans - winsAgainstShamans
    winsAgainstMages = df.loc[df['enemyPlayerClass1'] == 'MAGE', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'MAGE', 'win'].sum()
    lossesAgainstMages = gamesAgainstMages - winsAgainstMages
    winsAgainstWarlocks = df.loc[df['enemyPlayerClass1'] == 'WARLOCK', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'WARLOCK', 'win'].sum()
    lossesAgainstWarlocks = gamesAgainstWarlocks - winsAgainstWarlocks
    winsAgainstDruids = df.loc[df['enemyPlayerClass1'] == 'DRUID', 'win'].sum() + df.loc[df['enemyPlayerClass2'] == 'DRUID', 'win'].sum()
    lossesAgainstDruids = gamesAgainstDruids - winsAgainstDruids

    warriorWinRate = winsAgainstWarriors / gamesAgainstWarriors
    paladinWinRate = winsAgainstPaladins / gamesAgainstPaladins
    hunterWinRate = winsAgainstHunters / gamesAgainstHunters
    rogueWinRate = winsAgainstRogues / gamesAgainstRogues
    priestWinRate = winsAgainstPriests / gamesAgainstPriests
    deathKnightWinRate = winsAgainstDeathKnights / gamesAgainstDeathKnights
    shamanWinRate = winsAgainstShamans / gamesAgainstShamans
    mageWinRate = winsAgainstMages / gamesAgainstMages
    warlockWinRate = winsAgainstWarlocks / gamesAgainstWarlocks
    druidWinRate = winsAgainstDruids / gamesAgainstDruids
    return {
        'wins': wins,
        'losses': losses,
        'winRate': rate,
        'warriorWinRate': warriorWinRate,
        'paladinWinRate': paladinWinRate,
        'hunterWinRate': hunterWinRate,
        'rogueWinRate': rogueWinRate,
        'priestWinRate': priestWinRate,
        'deathKnightWinRate': deathKnightWinRate,
        'shamanWinRate': shamanWinRate,
        'mageWinRate': mageWinRate,
        'warlockWinRate': warlockWinRate,
        'druidWinRate': druidWinRate
    }



def calculate_comp_win_rates(df: pd.DataFrame) -> dict:
    allPossibleComps = list(combinations(['WARRIOR', 'PALADIN', 'HUNTER', 'ROGUE', 'PRIEST', 'DEATHKNIGHT', 'SHAMAN', 'MAGE', 'WARLOCK', 'DRUID'], 2))
    # print(allPossibleComps)
    winRates = {}
    for comp in allPossibleComps:
        gamesAgainstComp = len(df.loc[(df['enemyPlayerClass1'] == comp[0]) & (df['enemyPlayerClass2'] == comp[1])]) + len(df.loc[(df['enemyPlayerClass1'] == comp[1]) & (df['enemyPlayerClass2'] == comp[0])])
        winsAgainstComp = df.loc[(df['enemyPlayerClass1'] == comp[0]) & (df['enemyPlayerClass2'] == comp[1]), 'win'].sum() + df.loc[(df['enemyPlayerClass1'] == comp[1]) & (df['enemyPlayerClass2'] == comp[0]), 'win'].sum()
        lossesAgainstComp = gamesAgainstComp - winsAgainstComp
        winRateAgainstComp = winsAgainstComp / gamesAgainstComp
        winRates[comp] = winRateAgainstComp
    return winRates
