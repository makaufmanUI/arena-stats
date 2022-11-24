import pandas as pd
import streamlit as st
#from functions import *
from matplotlib import pyplot as plt
from itertools import combinations

def parse_csv(csv):
    lines = csv.splitlines()
    lines.pop(0)
    headers = lines[0].split(',')
    rows = []
    for line in lines[1:]:
        row = line.split(',')
        row.pop(-1)
        rows.append(row)
    return pd.DataFrame(rows, columns=headers)



def simplify_dataframe(df):
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



def plot_rating(df, title = 'Rating', showEnemy = False):
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



def calculate_win_rates(df):
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



def calculate_comp_win_rates(df):
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


INPUT_TEXT = """
isRanked,startTime,endTime,zoneId,duration,teamName,teamColor,winnerColor,teamPlayerName1,teamPlayerName2,teamPlayerName3,teamPlayerName4,teamPlayerName5,teamPlayerClass1,teamPlayerClass2,teamPlayerClass3,teamPlayerClass4,teamPlayerClass5,teamPlayerRace1,teamPlayerRace2,teamPlayerRace3,teamPlayerRace4,teamPlayerRace5,oldTeamRating,newTeamRating,diffRating,mmr,enemyOldTeamRating,enemyNewTeamRating,enemyDiffRating,enemyMmr,enemyTeamName,enemyPlayerName1,enemyPlayerName2,enemyPlayerName3,enemyPlayerName4,enemyPlayerName5,enemyPlayerClass1,enemyPlayerClass2,enemyPlayerClass3,enemyPlayerClass4,enemyPlayerClass5,enemyPlayerRace1,enemyPlayerRace2,enemyPlayerRace3,enemyPlayerRace4,enemyPlayerRace5,enemyFaction
YES,1668979677,1668979814,559,137,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1223,1212,-11,1240,1272,1283,11,1251,,Grumpylunkns-Whitemane,Limpyllama-Whitemane,,,,DRUID,PRIEST,,,,TAUREN,UNDEAD,,,,HORDE,
YES,1668979903,1668980024,562,121,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1212,1200,-12,1215,1185,1201,16,1215,,Initially-Eranikus,Lichqueén-Eranikus,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,BLOODELF,,,,HORDE,
YES,1668980024,1668980151,572,127,,GOLD,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1200,1212,12,1188,1160,1149,-11,1190,,Shankmor-Eranikus,Summonlight-Eranikus,,,,ROGUE,PALADIN,,,,UNDEAD,BLOODELF,,,,HORDE,
YES,1668980152,1668980336,562,184,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1213,1201,-12,1215,1236,1247,11,1220,,Eldredx-Grobbulus,Holybeast-Grobbulus,,,,ROGUE,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1668980336,1668980460,617,124,,GREEN,GREEN,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1201,1212,11,1189,1138,1128,-10,1183,,Benjackinit-Sulfuras,Lemonshock-Sulfuras,,,,MAGE,SHAMAN,,,,GNOME,DRAENEI,,,,ALLIANCE,
YES,1668980460,1668980637,562,177,,GOLD,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1214,1226,12,1215,1176,1165,-11,1205,,Kyry-OldBlanchy,Lovestospoge-OldBlanchy,,,,DRUID,SHAMAN,,,,TAUREN,TROLL,,,,HORDE,
YES,1668980637,1668980799,562,162,,GOLD,GOLD,Drpain,Cope,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1228,1247,19,1240,866,866,0,1384,,Deathrollz-Benediction,Whortitude-Benediction,,,,WARRIOR,PRIEST,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1668980799,1668981169,617,370,,GOLD,GREEN,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1249,1238,-11,1280,1330,1340,10,1284,,Dkwhopper-Eranikus,Tootybooty-Eranikus,,,,DEATHKNIGHT,PRIEST,,,,BLOODELF,UNDEAD,,,,HORDE,
YES,1668981170,1668981319,572,149,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1238,1226,-12,1255,1087,1129,42,1252,,Mindmandarin-Benediction,Rhapsodyx-Benediction,,,,PALADIN,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1668981320,1668981439,559,119,,GOLD,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1226,1238,12,1228,1233,1221,-12,1228,,Bruiñ-Benediction,Ectriir-Benediction,,,,DRUID,HUNTER,,,,NIGHTELF,NIGHTELF,,,,ALLIANCE,
YES,1669084384,1669084472,617,88,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1297,1309,12,1290,1284,1272,-12,1287,,Bowadin-Mankrik,Haikudied-Mankrik,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,ORC,,,,HORDE,
YES,1669084472,1669084659,617,187,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1309,1323,14,1316,1298,1287,-11,1331,,Kånye-Whitemane,Skîp-Whitemane,,,,ROGUE,PALADIN,,,,UNDEAD,BLOODELF,,,,HORDE,
YES,1669084659,1669084969,572,310,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1322,1311,-11,1345,1393,1403,10,1354,,Desttripador,Leopardd,,,,WARRIOR,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669084969,1669085131,572,162,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1311,1325,14,1320,1255,1245,-10,1328,,Byrndrop-Sulfuras,Fluabu-Sulfuras,,,,PRIEST,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1669085131,1669085346,562,215,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1325,1340,15,1347,1377,1364,-13,1348,,Avelorà-Benediction,Fingersteak-Benediction,,,,PRIEST,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1669085346,1669085916,572,570,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1340,1357,17,1374,1347,1336,-11,1370,,Bigdaddý-Faerlina,Gampi-Faerlina,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE,
YES,1669085916,1669086147,572,231,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1357,1346,-11,1399,1374,1388,14,1385,,Togepi-Benediction,Puppylion-Benediction,,,,PALADIN,HUNTER,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1669086147,1669086361,562,214,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1346,1335,-11,1371,1386,1397,11,1370,,Xpn-Grobbulus,Oeii-Grobbulus,,,,DEATHKNIGHT,PRIEST,,,,ORC,UNDEAD,,,,HORDE,
YES,1669086361,1669086501,559,140,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1335,1348,13,1345,1283,1273,-10,1337,,Moolander,Snarff,,,,DRUID,DEATHKNIGHT,,,,TAUREN,ORC,,,,HORDE,
YES,1669086501,1669086691,617,190,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1348,1363,15,1370,1372,1360,-12,1364,,Billybuffalo-Whitemane,Nefi-Whitemane,,,,MAGE,PRIEST,,,,UNDEAD,BLOODELF,,,,HORDE,
YES,1669086691,1669086981,562,290,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1363,1380,17,1395,1430,1417,-13,1406,,Boshea-Eranikus,Slimreap-Eranikus,,,,ROGUE,MAGE,,,,UNDEAD,UNDEAD,,,,HORDE,
YES,1669086981,1669087172,559,191,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1381,1370,-11,1423,1432,1444,12,1422,,Quikseven-Sulfuras,Drinkbooze-Sulfuras,,,,PRIEST,SHAMAN,,,,DRAENEI,DRAENEI,,,,ALLIANCE,
YES,1669087172,1669087314,617,142,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1370,1386,16,1397,1412,1399,-13,1401,,Christus-Pagle,Loganitus-Pagle,,,,PRIEST,WARRIOR,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669087314,1669087746,617,432,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1387,1404,17,1423,1368,1358,-10,1423,,Akiopal-Windseeker,Ratmovie-Windseeker,,,,PALADIN,WARRIOR,,,,BLOODELF,ORC,,,,HORDE,
YES,1669087746,1669089042,617,1296,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1404,1432,28,1450,948,948,0,1685,,Jvsxn-Benediction,Tankokingg-Benediction,,,,ROGUE,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669089043,1669089234,562,191,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1432,1423,-9,1494,1436,1459,23,1513,,Johnnybreeco-Faerlina,Urlacherx-Faerlina,,,,DRUID,PRIEST,,,,TAUREN,TROLL,,,,HORDE,
YES,1669089234,1669089512,572,278,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1423,1413,-10,1471,1333,1369,36,1471,,Cheetos,Beatriz,,,,SHAMAN,PALADIN,,,,ORC,BLOODELF,,,,HORDE,
YES,1669089512,1669089797,559,285,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1413,1402,-11,1445,1463,1474,11,1440,,Daddydivine-Sulfuras,Saketome-Sulfuras,,,,PALADIN,WARRIOR,,,,BLOODELF,TAUREN,,,,HORDE,
YES,1669089798,1669090293,559,495,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1402,1391,-11,1418,1425,1437,12,1420,,Cannie-Benediction,Thebossheale-Benediction,,,,WARRIOR,PALADIN,,,,GNOME,HUMAN,,,,ALLIANCE,
YES,1669090293,1669090872,562,579,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1391,1403,12,1392,1342,1332,-10,1390,,Donaldj-Grobbulus,Malamis-Grobbulus,,,,WARRIOR,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1669090872,1669091134,572,262,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1403,1417,14,1418,1419,1407,-12,1424,,Littlej-Benediction,Vysenya-Benediction,,,,MAGE,PRIEST,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669091134,1669091282,562,148,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1418,1434,16,1445,1409,1398,-11,1448,,Blastingdk-Whitemane,Manbearpally-Whitemane,,,,DEATHKNIGHT,PALADIN,,,,TROLL,BLOODELF,,,,HORDE,
YES,1669091282,1669091490,562,208,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1434,1423,-11,1472,1492,1503,11,1459,,Nhojx-Mankrik,Roons-Mankrik,,,,PRIEST,MAGE,,,,UNDEAD,UNDEAD,,,,HORDE,
YES,1669091490,1669091671,572,181,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1423,1438,15,1444,1405,1394,-11,1440,,Flexso-Sulfuras,Watchxlearn-Sulfuras,,,,PRIEST,DEATHKNIGHT,,,,UNDEAD,ORC,,,,HORDE,
YES,1669091671,1669091927,617,256,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1438,1427,-11,1469,1479,1491,12,1477,,Rbko,Saiyana,,,,DRUID,PRIEST,,,,NIGHTELF,HUMAN,,,,ALLIANCE,
YES,1669091927,1669092247,572,320,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1427,1416,-11,1444,1416,1432,16,1444,,Sanc-Grobbulus,Wxx-Grobbulus,,,,PALADIN,WARRIOR,,,,BLOODELF,ORC,,,,HORDE,
YES,1669092247,1669092459,562,212,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1416,1404,-12,1418,1423,1435,12,1418,,Arenaslave-Benediction,Blizrdsuport-Benediction,,,,DRUID,PRIEST,,,,NIGHTELF,HUMAN,,,,ALLIANCE,
YES,1669092459,1669092769,562,310,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1404,1392,-12,1392,1385,1398,13,1393,,Eldinora-Eranikus,Murderstein-Eranikus,,,,ROGUE,PRIEST,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669092769,1669092983,617,214,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1392,1379,-13,1366,1439,1449,10,1373,,Kyogen-Grobbulus,Reyädon-Grobbulus,,,,PRIEST,ROGUE,,,,UNDEAD,UNDEAD,,,,HORDE,
YES,1669252113,1669252484,562,371,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1379,1366,-13,1350,1338,1352,14,1352,,Dunkr-Grobbulus,Horndoggie-Grobbulus,,,,WARRIOR,DRUID,,,,TROLL,TAUREN,,,,HORDE,
YES,1669252485,1669253108,562,623,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1366,1377,11,1324,1310,1298,-12,1332,,Blackthòrn-Grobbulus,Hotdog-Grobbulus,,,,PALADIN,WARRIOR,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669253108,1669253601,559,493,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1377,1387,10,1352,1369,1356,-13,1332,,Ogruzin-Eranikus,Palabranco-Eranikus,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE,
YES,1669253601,1669253922,617,321,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1388,1375,-13,1375,1361,1375,14,1372,,Orvilledk-Whitemane,Raaged-Whitemane,,,,DEATHKNIGHT,PRIEST,,,,ORC,UNDEAD,,,,HORDE,
YES,1669253923,1669254217,559,294,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1375,1386,11,1348,1353,1341,-12,1345,,Brocodex-Earthfury,Deadbutt-Earthfury,,,,PRIEST,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669254217,1669254392,572,175,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1386,1402,16,1374,943,943,0,1500,,Dhaverik-Earthfury,Rëkriah-Earthfury,,,,DEATHKNIGHT,SHAMAN,,,,HUMAN,DRAENEI,,,,ALLIANCE,
YES,1669254392,1669254569,562,177,,GREEN,GOLD,Cope,,,,,DEATHKNIGHT,,,,,HUMAN,,,,,1402,1391,-11,1415,1453,1464,11,1436,,Rackmove-Benediction,Ruis-Benediction,,,,PALADIN,PRIEST,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669254570,1669255139,562,569,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1391,1403,12,1392,1392,1380,-12,1395,,Kyloret-Atiesh,Loserrogues-Atiesh,,,,PALADIN,SHAMAN,,,,BLOODELF,TAUREN,,,,HORDE,
YES,1669255140,1669255427,617,287,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1403,1392,-11,1418,1424,1436,12,1428,,Ciej-Faerlina,Läte-Faerlina,,,,PALADIN,WARRIOR,,,,BLOODELF,UNDEAD,,,,HORDE,
YES,1669255428,1669255803,559,375,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1392,1404,12,1394,1362,1351,-11,1389,,Eilf-Grobbulus,Revwenged-Grobbulus,,,,PALADIN,WARRIOR,,,,BLOODELF,ORC,,,,HORDE,
YES,1669255803,1669255989,559,186,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1404,1393,-11,1419,1418,1433,15,1447,,Drdisfigure-Westfall,Comfypillow-Westfall,,,,DEATHKNIGHT,PRIEST,,,,HUMAN,DWARF,,,,ALLIANCE,
YES,1669255990,1669256157,572,167,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1394,1382,-12,1397,1380,1395,15,1406,,Latersqt-Whitemane,Pfunq-Whitemane,,,,DRUID,MAGE,,,,TAUREN,UNDEAD,,,,HORDE,
YES,1669256158,1669256463,559,305,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1382,1393,11,1372,1321,1311,-10,1365,,Irkbaby-Mankrik,Vevern-Mankrik,,,,WARRIOR,PRIEST,,,,ORC,UNDEAD,,,,HORDE,
YES,1669256463,1669256803,562,340,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1393,1406,13,1397,1396,1384,-12,1400,,Holyskwabz-Faerlina,Valdeath-Faerlina,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,TAUREN,,,,HORDE,
YES,1669256803,1669257032,562,229,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1406,1421,15,1424,1446,1433,-13,1445,,Finnicon-Faerlina,Szm-Faerlina,,,,WARLOCK,SHAMAN,,,,ORC,TAUREN,,,,HORDE,
YES,1669257033,1669257428,559,395,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1421,1410,-11,1453,1442,1454,12,1443,,Zugsnotdrugs-Eranikus,Raeghar-Eranikus,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE,
YES,1669257429,1669257570,617,141,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1410,1425,15,1426,1476,1462,-14,1434,,Daysix-Benediction,Devvlol-Benediction,,,,ROGUE,MAGE,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669257571,1669257739,572,168,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1425,1414,-11,1453,1419,1436,17,1451,,Jpon-Grobbulus,Wetardid-Grobbulus,,,,ROGUE,PRIEST,,,,UNDEAD,UNDEAD,,,,HORDE,
YES,1669257739,1669257929,572,190,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1414,1402,-12,1427,1381,1400,19,1427,,Literalalien-Faerlina,Thiccpawg-Faerlina,,,,SHAMAN,PALADIN,,,,ORC,BLOODELF,,,,HORDE,
YES,1669257930,1669258158,559,228,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1402,1414,12,1400,1426,1413,-13,1404,,Meista-Grobbulus,Snipergoat-Grobbulus,,,,PRIEST,HUNTER,,,,DRAENEI,DRAENEI,,,,ALLIANCE,
YES,1669258158,1669258873,562,715,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1414,1402,-12,1427,1428,1440,12,1424,,Fjp-Faerlina,Shlonk-Faerlina,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE,
YES,1669258873,1669259079,562,206,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1402,1414,12,1400,1377,1366,-11,1398,,Skyeatsyou,Thully,,,,WARLOCK,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1669259079,1669259599,617,520,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1414,1428,14,1426,1450,1437,-13,1429,,Cleare-Eranikus,Haakaii-Eranikus,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,TROLL,,,,HORDE,
YES,1669259599,1669259839,572,240,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1428,1444,16,1453,1385,1375,-10,1455,,Mazecrazed-Maladath,Profits-Maladath,,,,PRIEST,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669259839,1669260105,617,266,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1444,1433,-11,1480,1461,1475,14,1472,,Turtlefood-Benediction,Jesxr-Benediction,,,,WARRIOR,PALADIN,,,,GNOME,HUMAN,,,,ALLIANCE,
YES,1669260105,1669260385,562,280,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1433,1421,-12,1452,1369,1394,25,1446,,Tiána-Sulfuras,Jiraff-Sulfuras,,,,PALADIN,PRIEST,,,,BLOODELF,BLOODELF,,,,HORDE,
YES,1669260386,1669260620,617,234,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1421,1408,-13,1425,1421,1433,12,1402,,Ghear-Mankrik,Impaleinside-Mankrik,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,ORC,,,,HORDE,
YES,1669260620,1669260806,572,186,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1408,1420,12,1395,1369,1358,-11,1399,,Crïxús-Earthfury,Spärtäcus-Earthfury,,,,PALADIN,WARRIOR,,,,HUMAN,HUMAN,,,,ALLIANCE,
YES,1669260806,1669261014,572,208,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1420,1432,12,1422,1461,1448,-13,1416,,Ozsake-Grobbulus,Vets-Grobbulus,,,,MAGE,ROGUE,,,,UNDEAD,UNDEAD,,,,HORDE,
YES,1669261014,1669261190,559,176,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1432,1420,-12,1447,1409,1426,17,1438,,Defuhx-Grobbulus,Fatshift-Grobbulus,,,,ROGUE,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
YES,1669261190,1669261395,617,205,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1420,1408,-12,1420,1388,1405,17,1426,,Tihshew-Benediction,Kootzz-Benediction,,,,WARRIOR,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE,
"""




#st.set_page_config(page_title="Arena Stats",layout="centered",page_icon=":crossed_swords:")
df = parse_csv(INPUT_TEXT)
df = simplify_dataframe(df)
st.markdown("# Arena Stats")
st.markdown("---")

st.markdown("## Comp winrates")
st.markdown("---")
st.write("")
comp_winrates = calculate_comp_win_rates(df)
for comp, winrate in comp_winrates.items():
    if winrate > 0:
        st.write(f"{comp[0].title()}, {comp[1].title()} :  {winrate*100:.2f}%")

st.write("")


    
st.markdown("## Rating over time")
fig, ax = plt.subplots()
ratings = df['oldTeamRating'].astype(int)
ax.plot(ratings)
st.pyplot(fig)
