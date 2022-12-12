import pandas as pd
from functions import sort_tuple





def parse_csv(csv: str) -> pd.DataFrame:
    # lines = csv.splitlines()
    # lines = '\n'.join(csv)
    lines = csv.splitlines()
    # lines.pop(0)
    headers = lines[0].split(',')
    rows = []
    for line in lines[1:]:
        row = line.split(',')
        row.pop(-1)
        rows.append(row)
    return pd.DataFrame(rows, columns=headers)





def cleanup_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['win'] = df['teamColor'] == df['winnerColor']
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df = df.drop(columns=['teamColor', 'winnerColor', 'enemyFaction'])
    df = df.drop(columns=['isRanked', 'startTime', 'endTime', 'zoneId', 'teamName', 'enemyTeamName'])
    df = df.drop(columns=['teamPlayerName1', 'teamPlayerName2', 'teamPlayerName3'])
    df = df.drop(columns=['enemyPlayerName1', 'enemyPlayerName2', 'enemyPlayerName3'])
    df = df.drop(columns=['teamPlayerName4', 'teamPlayerName5', 'enemyPlayerName4', 'enemyPlayerName5'])
    df = df.drop(columns=['teamPlayerRace4', 'teamPlayerRace5', 'enemyPlayerRace4', 'enemyPlayerRace5'])
    df = df.drop(columns=['teamPlayerRace1', 'teamPlayerRace2', 'teamPlayerRace3'])
    df = df.drop(columns=['enemyPlayerRace1', 'enemyPlayerRace2', 'enemyPlayerRace3'])
    df = df.drop(columns=['teamPlayerClass4', 'teamPlayerClass5', 'enemyPlayerClass4', 'enemyPlayerClass5'])
    # reorder the teamPlayerClass and enempyPlayerClass columns so they are alphabetical
    combined_list = list(zip(df['teamPlayerClass1'].tolist(), df['teamPlayerClass2'].tolist(), df['teamPlayerClass3'].tolist()))
    new_list = []
    for comp in combined_list:
        new_comp = sort_tuple(comp)
        if new_comp[0] == '':   # if the first element is a blank string, move it to the end
            new_comp = new_comp[1:] + new_comp[:1]
        new_list.append(new_comp)
    df['teamPlayerClass1'], df['teamPlayerClass2'], df['teamPlayerClass3'] = zip(*new_list)
    combined_list = list(zip(df['enemyPlayerClass1'].tolist(), df['enemyPlayerClass2'].tolist(), df['enemyPlayerClass3'].tolist()))
    new_list = []
    for comp in combined_list:
        new_comp = sort_tuple(comp)
        if new_comp[0] == '':
            new_comp = new_comp[1:] + new_comp[:1]
        new_list.append(new_comp)
    df['enemyPlayerClass1'], df['enemyPlayerClass2'], df['enemyPlayerClass3'] = zip(*new_list)
    return df




def get_2v2_matches(df: pd.DataFrame) -> pd.DataFrame:
    data = df[df['teamPlayerClass3'] == '']
    data = data.reset_index(drop=True)
    return data




def get_3v3_matches(df: pd.DataFrame) -> pd.DataFrame:
    data = df[df['teamPlayerClass3'] != '']
    data = data.reset_index(drop=True)
    return data





def get_3v3_comps(df: pd.DataFrame) -> pd.DataFrame:
    comps = list(zip(df['enemyPlayerClass1'].tolist(), df['enemyPlayerClass2'].tolist(), df['enemyPlayerClass3'].tolist()))
    unique_comps = set(comps)   # get just the unique comps
    return list(unique_comps)





def get_3v3_comps_data(df: pd.DataFrame) -> dict:
    comps = get_3v3_comps(df)
    data = {}
    for comp in comps:
        data[','.join(comp)] = df[(df['enemyPlayerClass1'] == comp[0]) & (df['enemyPlayerClass2'] == comp[1]) & (df['enemyPlayerClass3'] == comp[2])].to_dict()
    return data





def get_3v3_comps_winrates(df: pd.DataFrame) -> dict:
    comps_data = get_3v3_comps_data(df)
    winrates = {}
    for comp in comps_data:
        wins = 0
        losses = 0
        keys = list(comps_data[comp]['win'].keys())
        for i in range(len(comps_data[comp]['win'])):
            if comps_data[comp]['win'][keys[i]]:
                wins += 1
            else:
                losses += 1
        winrates[comp] = wins / (wins + losses)
    # sort the winrates by value
    winrates = dict(sorted(winrates.items(), key=lambda item: item[1], reverse=True))
    return winrates




def simplify_data(df: pd.DataFrame, arena_size: int = 3) -> pd.DataFrame:
    df = df.copy()
    df = df.loc[:, (df != '').any(axis=0)]
    df = df.drop(columns=['isRanked', 'startTime', 'endTime', 'zoneId'])
    df = df.drop(columns=['enemyPlayerName1', 'enemyPlayerName2'])
    df = df.drop(columns=['teamPlayerRace1' , 'teamPlayerRace2', 'enemyPlayerRace1', 'enemyPlayerRace2'])
    df = df.drop(columns=['teamPlayerName1' , 'teamPlayerName2', 'teamPlayerClass1', 'teamPlayerClass2', 'enemyFaction'])
    if arena_size == 3:
        df = df.drop(columns=['enemyPlayerName3'])
        df = df.drop(columns=['teamPlayerRace3', 'enemyPlayerRace3'])
        df = df.drop(columns=['teamPlayerName3', 'teamPlayerClass3'])
    # df = df.iloc[10:]
    # df = df.copy().reset_index(drop=True)
    df['win'] = df['teamColor'] == df['winnerColor']
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df = df.drop(columns=['teamColor', 'winnerColor'])
    
    df = df.drop(columns=['newTeamRating', 'mmr', 'enemyNewTeamRating', 'enemyDiffRating', 'enemyMmr', 'enemyPlayerName1', 'enemyPlayerName2'])
    return df







TEST_DATA = r"isRanked,startTime,endTime,zoneId,duration,teamName,teamColor,winnerColor,teamPlayerName1,teamPlayerName2,teamPlayerName3,teamPlayerName4,teamPlayerName5,teamPlayerClass1,teamPlayerClass2,teamPlayerClass3,teamPlayerClass4,teamPlayerClass5,teamPlayerRace1,teamPlayerRace2,teamPlayerRace3,teamPlayerRace4,teamPlayerRace5,oldTeamRating,newTeamRating,diffRating,mmr,enemyOldTeamRating,enemyNewTeamRating,enemyDiffRating,enemyMmr,enemyTeamName,enemyPlayerName1,enemyPlayerName2,enemyPlayerName3,enemyPlayerName4,enemyPlayerName5,enemyPlayerClass1,enemyPlayerClass2,enemyPlayerClass3,enemyPlayerClass4,enemyPlayerClass5,enemyPlayerRace1,enemyPlayerRace2,enemyPlayerRace3,enemyPlayerRace4,enemyPlayerRace5,enemyFaction YES,1668979677,1668979814,559,137,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1223,1212,-11,1240,1272,1283,11,1251,,Grumpylunkns-Whitemane,Limpyllama-Whitemane,,,,DRUID,PRIEST,,,,TAUREN,UNDEAD,,,,HORDE, YES,1668979903,1668980024,562,121,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1212,1200,-12,1215,1185,1201,16,1215,,Initially-Eranikus,Lichqueén-Eranikus,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,BLOODELF,,,,HORDE, YES,1668980024,1668980151,572,127,,GOLD,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1200,1212,12,1188,1160,1149,-11,1190,,Shankmor-Eranikus,Summonlight-Eranikus,,,,ROGUE,PALADIN,,,,UNDEAD,BLOODELF,,,,HORDE, YES,1668980152,1668980336,562,184,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1213,1201,-12,1215,1236,1247,11,1220,,Eldredx-Grobbulus,Holybeast-Grobbulus,,,,ROGUE,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1668980336,1668980460,617,124,,GREEN,GREEN,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1201,1212,11,1189,1138,1128,-10,1183,,Benjackinit-Sulfuras,Lemonshock-Sulfuras,,,,MAGE,SHAMAN,,,,GNOME,DRAENEI,,,,ALLIANCE, YES,1668980460,1668980637,562,177,,GOLD,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1214,1226,12,1215,1176,1165,-11,1205,,Kyry-OldBlanchy,Lovestospoge-OldBlanchy,,,,DRUID,SHAMAN,,,,TAUREN,TROLL,,,,HORDE, YES,1668980637,1668980799,562,162,,GOLD,GOLD,Drpain,Cope,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1228,1247,19,1240,866,866,0,1384,,Deathrollz-Benediction,Whortitude-Benediction,,,,WARRIOR,PRIEST,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1668980799,1668981169,617,370,,GOLD,GREEN,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1249,1238,-11,1280,1330,1340,10,1284,,Dkwhopper-Eranikus,Tootybooty-Eranikus,,,,DEATHKNIGHT,PRIEST,,,,BLOODELF,UNDEAD,,,,HORDE, YES,1668981170,1668981319,572,149,,GREEN,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1238,1226,-12,1255,1087,1129,42,1252,,Mindmandarin-Benediction,Rhapsodyx-Benediction,,,,PALADIN,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1668981320,1668981439,559,119,,GOLD,GOLD,Cope,Drpain,,,,DEATHKNIGHT,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1226,1238,12,1228,1233,1221,-12,1228,,Bruiñ-Benediction,Ectriir-Benediction,,,,DRUID,HUNTER,,,,NIGHTELF,NIGHTELF,,,,ALLIANCE, YES,1669084384,1669084472,617,88,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1297,1309,12,1290,1284,1272,-12,1287,,Bowadin-Mankrik,Haikudied-Mankrik,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,ORC,,,,HORDE, YES,1669084472,1669084659,617,187,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1309,1323,14,1316,1298,1287,-11,1331,,Kånye-Whitemane,Skîp-Whitemane,,,,ROGUE,PALADIN,,,,UNDEAD,BLOODELF,,,,HORDE, YES,1669084659,1669084969,572,310,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1322,1311,-11,1345,1393,1403,10,1354,,Desttripador,Leopardd,,,,WARRIOR,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669084969,1669085131,572,162,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1311,1325,14,1320,1255,1245,-10,1328,,Byrndrop-Sulfuras,Fluabu-Sulfuras,,,,PRIEST,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669085131,1669085346,562,215,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1325,1340,15,1347,1377,1364,-13,1348,,Avelorà-Benediction,Fingersteak-Benediction,,,,PRIEST,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669085346,1669085916,572,570,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1340,1357,17,1374,1347,1336,-11,1370,,Bigdaddý-Faerlina,Gampi-Faerlina,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669085916,1669086147,572,231,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1357,1346,-11,1399,1374,1388,14,1385,,Togepi-Benediction,Puppylion-Benediction,,,,PALADIN,HUNTER,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669086147,1669086361,562,214,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1346,1335,-11,1371,1386,1397,11,1370,,Xpn-Grobbulus,Oeii-Grobbulus,,,,DEATHKNIGHT,PRIEST,,,,ORC,UNDEAD,,,,HORDE, YES,1669086361,1669086501,559,140,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1335,1348,13,1345,1283,1273,-10,1337,,Moolander,Snarff,,,,DRUID,DEATHKNIGHT,,,,TAUREN,ORC,,,,HORDE, YES,1669086501,1669086691,617,190,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1348,1363,15,1370,1372,1360,-12,1364,,Billybuffalo-Whitemane,Nefi-Whitemane,,,,MAGE,PRIEST,,,,UNDEAD,BLOODELF,,,,HORDE, YES,1669086691,1669086981,562,290,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1363,1380,17,1395,1430,1417,-13,1406,,Boshea-Eranikus,Slimreap-Eranikus,,,,ROGUE,MAGE,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669086981,1669087172,559,191,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1381,1370,-11,1423,1432,1444,12,1422,,Quikseven-Sulfuras,Drinkbooze-Sulfuras,,,,PRIEST,SHAMAN,,,,DRAENEI,DRAENEI,,,,ALLIANCE, YES,1669087172,1669087314,617,142,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1370,1386,16,1397,1412,1399,-13,1401,,Christus-Pagle,Loganitus-Pagle,,,,PRIEST,WARRIOR,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669087314,1669087746,617,432,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1387,1404,17,1423,1368,1358,-10,1423,,Akiopal-Windseeker,Ratmovie-Windseeker,,,,PALADIN,WARRIOR,,,,BLOODELF,ORC,,,,HORDE, YES,1669087746,1669089042,617,1296,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1404,1432,28,1450,948,948,0,1685,,Jvsxn-Benediction,Tankokingg-Benediction,,,,ROGUE,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669089043,1669089234,562,191,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1432,1423,-9,1494,1436,1459,23,1513,,Johnnybreeco-Faerlina,Urlacherx-Faerlina,,,,DRUID,PRIEST,,,,TAUREN,TROLL,,,,HORDE, YES,1669089234,1669089512,572,278,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1423,1413,-10,1471,1333,1369,36,1471,,Cheetos,Beatriz,,,,SHAMAN,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669089512,1669089797,559,285,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1413,1402,-11,1445,1463,1474,11,1440,,Daddydivine-Sulfuras,Saketome-Sulfuras,,,,PALADIN,WARRIOR,,,,BLOODELF,TAUREN,,,,HORDE, YES,1669089798,1669090293,559,495,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1402,1391,-11,1418,1425,1437,12,1420,,Cannie-Benediction,Thebossheale-Benediction,,,,WARRIOR,PALADIN,,,,GNOME,HUMAN,,,,ALLIANCE, YES,1669090293,1669090872,562,579,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1391,1403,12,1392,1342,1332,-10,1390,,Donaldj-Grobbulus,Malamis-Grobbulus,,,,WARRIOR,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669090872,1669091134,572,262,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1403,1417,14,1418,1419,1407,-12,1424,,Littlej-Benediction,Vysenya-Benediction,,,,MAGE,PRIEST,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669091134,1669091282,562,148,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1418,1434,16,1445,1409,1398,-11,1448,,Blastingdk-Whitemane,Manbearpally-Whitemane,,,,DEATHKNIGHT,PALADIN,,,,TROLL,BLOODELF,,,,HORDE, YES,1669091282,1669091490,562,208,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1434,1423,-11,1472,1492,1503,11,1459,,Nhojx-Mankrik,Roons-Mankrik,,,,PRIEST,MAGE,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669091490,1669091671,572,181,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1423,1438,15,1444,1405,1394,-11,1440,,Flexso-Sulfuras,Watchxlearn-Sulfuras,,,,PRIEST,DEATHKNIGHT,,,,UNDEAD,ORC,,,,HORDE, YES,1669091671,1669091927,617,256,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1438,1427,-11,1469,1479,1491,12,1477,,Rbko,Saiyana,,,,DRUID,PRIEST,,,,NIGHTELF,HUMAN,,,,ALLIANCE, YES,1669091927,1669092247,572,320,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1427,1416,-11,1444,1416,1432,16,1444,,Sanc-Grobbulus,Wxx-Grobbulus,,,,PALADIN,WARRIOR,,,,BLOODELF,ORC,,,,HORDE, YES,1669092247,1669092459,562,212,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1416,1404,-12,1418,1423,1435,12,1418,,Arenaslave-Benediction,Blizrdsuport-Benediction,,,,DRUID,PRIEST,,,,NIGHTELF,HUMAN,,,,ALLIANCE, YES,1669092459,1669092769,562,310,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1404,1392,-12,1392,1385,1398,13,1393,,Eldinora-Eranikus,Murderstein-Eranikus,,,,ROGUE,PRIEST,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669092769,1669092983,617,214,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1392,1379,-13,1366,1439,1449,10,1373,,Kyogen-Grobbulus,Reyädon-Grobbulus,,,,PRIEST,ROGUE,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669252113,1669252484,562,371,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1379,1366,-13,1350,1338,1352,14,1352,,Dunkr-Grobbulus,Horndoggie-Grobbulus,,,,WARRIOR,DRUID,,,,TROLL,TAUREN,,,,HORDE, YES,1669252485,1669253108,562,623,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1366,1377,11,1324,1310,1298,-12,1332,,Blackthòrn-Grobbulus,Hotdog-Grobbulus,,,,PALADIN,WARRIOR,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669253108,1669253601,559,493,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1377,1387,10,1352,1369,1356,-13,1332,,Ogruzin-Eranikus,Palabranco-Eranikus,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669253601,1669253922,617,321,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1388,1375,-13,1375,1361,1375,14,1372,,Orvilledk-Whitemane,Raaged-Whitemane,,,,DEATHKNIGHT,PRIEST,,,,ORC,UNDEAD,,,,HORDE, YES,1669253923,1669254217,559,294,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1375,1386,11,1348,1353,1341,-12,1345,,Brocodex-Earthfury,Deadbutt-Earthfury,,,,PRIEST,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669254217,1669254392,572,175,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1386,1402,16,1374,943,943,0,1500,,Dhaverik-Earthfury,Rëkriah-Earthfury,,,,DEATHKNIGHT,SHAMAN,,,,HUMAN,DRAENEI,,,,ALLIANCE, YES,1669254392,1669254569,562,177,,GREEN,GOLD,Cope,,,,,DEATHKNIGHT,,,,,HUMAN,,,,,1402,1391,-11,1415,1453,1464,11,1436,,Rackmove-Benediction,Ruis-Benediction,,,,PALADIN,PRIEST,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669254570,1669255139,562,569,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1391,1403,12,1392,1392,1380,-12,1395,,Kyloret-Atiesh,Loserrogues-Atiesh,,,,PALADIN,SHAMAN,,,,BLOODELF,TAUREN,,,,HORDE, YES,1669255140,1669255427,617,287,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1403,1392,-11,1418,1424,1436,12,1428,,Ciej-Faerlina,Läte-Faerlina,,,,PALADIN,WARRIOR,,,,BLOODELF,UNDEAD,,,,HORDE, YES,1669255428,1669255803,559,375,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1392,1404,12,1394,1362,1351,-11,1389,,Eilf-Grobbulus,Revwenged-Grobbulus,,,,PALADIN,WARRIOR,,,,BLOODELF,ORC,,,,HORDE, YES,1669255803,1669255989,559,186,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1404,1393,-11,1419,1418,1433,15,1447,,Drdisfigure-Westfall,Comfypillow-Westfall,,,,DEATHKNIGHT,PRIEST,,,,HUMAN,DWARF,,,,ALLIANCE, YES,1669255990,1669256157,572,167,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1394,1382,-12,1397,1380,1395,15,1406,,Latersqt-Whitemane,Pfunq-Whitemane,,,,DRUID,MAGE,,,,TAUREN,UNDEAD,,,,HORDE, YES,1669256158,1669256463,559,305,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1382,1393,11,1372,1321,1311,-10,1365,,Irkbaby-Mankrik,Vevern-Mankrik,,,,WARRIOR,PRIEST,,,,ORC,UNDEAD,,,,HORDE, YES,1669256463,1669256803,562,340,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1393,1406,13,1397,1396,1384,-12,1400,,Holyskwabz-Faerlina,Valdeath-Faerlina,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,TAUREN,,,,HORDE, YES,1669256803,1669257032,562,229,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1406,1421,15,1424,1446,1433,-13,1445,,Finnicon-Faerlina,Szm-Faerlina,,,,WARLOCK,SHAMAN,,,,ORC,TAUREN,,,,HORDE, YES,1669257033,1669257428,559,395,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1421,1410,-11,1453,1442,1454,12,1443,,Zugsnotdrugs-Eranikus,Raeghar-Eranikus,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669257429,1669257570,617,141,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1410,1425,15,1426,1476,1462,-14,1434,,Daysix-Benediction,Devvlol-Benediction,,,,ROGUE,MAGE,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669257571,1669257739,572,168,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1425,1414,-11,1453,1419,1436,17,1451,,Jpon-Grobbulus,Wetardid-Grobbulus,,,,ROGUE,PRIEST,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669257739,1669257929,572,190,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1414,1402,-12,1427,1381,1400,19,1427,,Literalalien-Faerlina,Thiccpawg-Faerlina,,,,SHAMAN,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669257930,1669258158,559,228,,GOLD,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1402,1414,12,1400,1426,1413,-13,1404,,Meista-Grobbulus,Snipergoat-Grobbulus,,,,PRIEST,HUNTER,,,,DRAENEI,DRAENEI,,,,ALLIANCE, YES,1669258158,1669258873,562,715,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1414,1402,-12,1427,1428,1440,12,1424,,Fjp-Faerlina,Shlonk-Faerlina,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669258873,1669259079,562,206,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1402,1414,12,1400,1377,1366,-11,1398,,Skyeatsyou,Thully,,,,WARLOCK,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669259079,1669259599,617,520,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1414,1428,14,1426,1450,1437,-13,1429,,Cleare-Eranikus,Haakaii-Eranikus,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,TROLL,,,,HORDE, YES,1669259599,1669259839,572,240,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1428,1444,16,1453,1385,1375,-10,1455,,Mazecrazed-Maladath,Profits-Maladath,,,,PRIEST,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669259839,1669260105,617,266,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1444,1433,-11,1480,1461,1475,14,1472,,Turtlefood-Benediction,Jesxr-Benediction,,,,WARRIOR,PALADIN,,,,GNOME,HUMAN,,,,ALLIANCE, YES,1669260105,1669260385,562,280,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1433,1421,-12,1452,1369,1394,25,1446,,Tiána-Sulfuras,Jiraff-Sulfuras,,,,PALADIN,PRIEST,,,,BLOODELF,BLOODELF,,,,HORDE, YES,1669260386,1669260620,617,234,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1421,1408,-13,1425,1421,1433,12,1402,,Ghear-Mankrik,Impaleinside-Mankrik,,,,PALADIN,DEATHKNIGHT,,,,BLOODELF,ORC,,,,HORDE, YES,1669260620,1669260806,572,186,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1408,1420,12,1395,1369,1358,-11,1399,,Crïxús-Earthfury,Spärtäcus-Earthfury,,,,PALADIN,WARRIOR,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669260806,1669261014,572,208,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1420,1432,12,1422,1461,1448,-13,1416,,Ozsake-Grobbulus,Vets-Grobbulus,,,,MAGE,ROGUE,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669261014,1669261190,559,176,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1432,1420,-12,1447,1409,1426,17,1438,,Defuhx-Grobbulus,Fatshift-Grobbulus,,,,ROGUE,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669261190,1669261395,617,205,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1420,1408,-12,1420,1388,1405,17,1426,,Tihshew-Benediction,Kootzz-Benediction,,,,WARRIOR,DRUID,,,,HUMAN,NIGHTELF,,,,ALLIANCE, YES,1669261395,1669261573,562,178,,GREEN,GREEN,Opsec,Cope,,,,PALADIN,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1408,1419,11,1394,1368,1357,-11,1386,,Janness-Faerlina,Josedeodo-Faerlina,,,,DRUID,ROGUE,,,,TAUREN,UNDEAD,,,,HORDE, YES,1669261573,1669261744,572,171,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1419,1407,-12,1419,1424,1437,13,1432,,Pantsdk-Benediction,Shmorpheus-Benediction,,,,DEATHKNIGHT,SHAMAN,,,,HUMAN,DRAENEI,,,,ALLIANCE, YES,1669261744,1669261887,572,143,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1407,1419,12,1395,1419,1406,-13,1395,,Fallend-Benediction,Potatoz-Benediction,,,,ROGUE,DRUID,,,,DWARF,NIGHTELF,,,,ALLIANCE, YES,1669261887,1669262187,562,300,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1419,1432,13,1421,1428,1416,-12,1432,,Dreamsphere-Westfall,Storyupbud-Westfall,,,,DRUID,PRIEST,,,,NIGHTELF,HUMAN,,,,ALLIANCE, YES,1669262187,1669262423,572,236,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1432,1421,-11,1449,1418,1435,17,1456,,Flexso-Sulfuras,Reggay-Sulfuras,,,,PRIEST,ROGUE,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669262423,1669262669,562,246,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1421,1409,-12,1424,1406,1420,14,1421,,Broloh-Grobbulus,Misunfortune-Grobbulus,,,,WARRIOR,PALADIN,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669262670,1669262830,559,160,,GOLD,GOLD,Opsec,Cope,,,,PALADIN,DEATHKNIGHT,,,,HUMAN,HUMAN,,,,1409,1420,11,1397,1359,1348,-11,1385,,Scamandrius-Whitemane,Vedran-Whitemane,,,,DRUID,ROGUE,,,,TAUREN,ORC,,,,HORDE, YES,1669262830,1669263020,559,190,,GREEN,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1420,1431,11,1422,1410,1398,-12,1397,,Gråy-Whitemane,Lootiez-Whitemane,,,,PRIEST,ROGUE,,,,UNDEAD,UNDEAD,,,,HORDE, YES,1669263020,1669263165,559,145,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1431,1420,-11,1444,1419,1436,17,1452,,Iamclutch-Faerlina,Krysm-Faerlina,,,,ROGUE,MAGE,,,,ORC,UNDEAD,,,,HORDE, YES,1669263165,1669263400,559,235,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1420,1408,-12,1419,1416,1428,12,1413,,Lolstorm-Whitemane,Ginster-Whitemane,,,,WARRIOR,PRIEST,,,,ORC,UNDEAD,,,,HORDE, YES,1669263401,1669263708,562,307,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1408,1396,-12,1392,1422,1433,11,1399,,Moonveilz-Sulfuras,Shuangpinai-Sulfuras,,,,DEATHKNIGHT,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669263708,1669264055,617,347,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1396,1383,-13,1367,1384,1395,11,1378,,Necrøspawn-Eranikus,Wooget-Eranikus,,,,DEATHKNIGHT,PRIEST,,,,ORC,UNDEAD,,,,HORDE, YES,1669264055,1669264765,562,710,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1383,1370,-13,1342,1338,1352,14,1353,,Majingassed-Grobbulus,Majinchown-Grobbulus,,,,HUNTER,PRIEST,,,,DWARF,DWARF,,,,ALLIANCE, YES,1669264765,1669264963,617,198,,GREEN,GOLD,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1370,1356,-14,1318,1299,1314,15,1324,,Zabbx-Pagle,Aurialle-Pagle,,,,PRIEST,ROGUE,,,,HUMAN,HUMAN,,,,ALLIANCE, YES,1669264964,1669265153,572,189,,GOLD,GREEN,Cope,Opsec,,,,DEATHKNIGHT,PALADIN,,,,HUMAN,HUMAN,,,,1356,1342,-14,1293,1286,1298,12,1287,,Booked-Eranikus,Pingutitan-Eranikus,,,,WARRIOR,PALADIN,,,,ORC,BLOODELF,,,,HORDE, YES,1669265153,1669265582,572,429,,GREEN,GREEN,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,459,552,93,1474,1011,1009,-2,1074,,Aldraenstein-Benediction,Cakesoap-Benediction,Iwannabeurgf-Benediction,,,SHAMAN,ROGUE,DRUID,,,DRAENEI,HUMAN,NIGHTELF,,,ALLIANCE, YES,1669265582,1669265792,559,210,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,524,619,95,1481,790,790,0,1346,,Kinëtic-Benediction,Naebliz-Benediction,Saigot-Benediction,,,ROGUE,PRIEST,PALADIN,,,HUMAN,HUMAN,HUMAN,,,ALLIANCE, YES,1669265793,1669266015,617,222,,GREEN,GREEN,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,592,685,93,1529,1001,1001,0,1217,,Doroxius-Mankrik,Fetacheesy-Mankrik,Halfwicked-Mankrik,,,PALADIN,DEATHKNIGHT,PRIEST,,,BLOODELF,BLOODELF,UNDEAD,,,HORDE, YES,1669266016,1669266214,617,198,,GREEN,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,658,751,93,1541,1003,1003,0,1255,,Freeduhm-Benediction,Loudpkjonson-Benediction,Tópgün-Benediction,,,PALADIN,DEATHKNIGHT,HUNTER,,,HUMAN,HUMAN,NIGHTELF,,,ALLIANCE, YES,1669266214,1669266656,562,442,,GREEN,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,724,818,94,1556,1068,1068,0,1360,,Shuswap-Grobbulus,Freerio-Grobbulus,Missginger-Grobbulus,,,PRIEST,WARLOCK,PALADIN,,,HUMAN,HUMAN,DWARF,,,ALLIANCE, YES,1669266656,1669266816,559,160,,GOLD,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,792,792,0,1584,1360,1379,19,1326,,Accierro,Hashey,Wetass,,,SHAMAN,DRUID,PRIEST,,,ORC,TAUREN,UNDEAD,,,HORDE, YES,1669266816,1669267012,572,196,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,787,876,89,1348,1256,1247,-9,1241,,Faulty-Eranikus,Felixdelao-Eranikus,Shinylol-Eranikus,,,PRIEST,WARLOCK,DRUID,,,HUMAN,HUMAN,NIGHTELF,,,ALLIANCE, YES,1669267012,1669267282,559,270,,GREEN,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,852,852,0,1395,1138,1183,45,1290,,Ebonlock-Eranikus,Unbalancéd-Eranikus,Syrs-Eranikus,,,WARLOCK,DRUID,SHAMAN,,,HUMAN,NIGHTELF,DRAENEI,,,ALLIANCE, YES,1669267282,1669267522,562,240,,GREEN,GREEN,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,847,941,94,1279,383,383,0,1523,,Pansitolk-Benediction,Redtesla-Benediction,Restinpissho-Benediction,,,DRUID,PRIEST,ROGUE,,,NIGHTELF,DWARF,HUMAN,,,ALLIANCE, YES,1669267522,1669267675,572,153,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,916,1003,87,1378,1287,1278,-9,1305,,Belpy-Grobbulus,Iluaanalaa-Grobbulus,Treelonmoosk-Grobbulus,,,DEATHKNIGHT,PRIEST,DRUID,,,ORC,TROLL,TAUREN,,,HORDE, YES,1669267675,1669267880,562,205,,GOLD,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,982,982,0,1419,1343,1359,16,1353,,Foxbody-Faerlina,Lappat-Faerlina,Saigry-Faerlina,,,DRUID,WARRIOR,PRIEST,,,TAUREN,ORC,UNDEAD,,,HORDE, YES,1669267880,1669268049,562,169,,GOLD,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,977,1059,82,1333,1099,1099,0,1285,,Gpie-Mankrik,Gutslugger-Mankrik,Iug-Mankrik,,,MAGE,SHAMAN,PRIEST,,,UNDEAD,ORC,UNDEAD,,,HORDE, YES,1669268049,1669268203,617,154,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1041,1120,79,1374,1262,1254,-8,1345,,Akagãmi-Westfall,Happysnus-Westfall,Holydietdew-Westfall,,,DEATHKNIGHT,MAGE,PALADIN,,,HUMAN,GNOME,HUMAN,,,ALLIANCE, YES,1669268203,1669268473,617,270,,GREEN,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1105,1105,0,1416,1410,1422,12,1395,,Bloodfang-Whitemane,Anorissaa-Whitemane,Pawn-Whitemane,,,WARRIOR,WARLOCK,PALADIN,,,ORC,UNDEAD,BLOODELF,,,HORDE, YES,1669268473,1669268740,572,267,,GREEN,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1100,1100,0,1361,1199,1240,41,1362,,Transformita-Whitemane,Formita-Whitemane,Chadbutgirl-Whitemane,,,WARRIOR,MAGE,PALADIN,,,ORC,BLOODELF,BLOODELF,,,HORDE, YES,1669268740,1669268910,572,170,,GREEN,GREEN,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1096,1151,55,1318,1327,1315,-12,1321,,Emblematic-Whitemane,Sylencia-Whitemane,Thermopops-Whitemane,,,PALADIN,WARLOCK,DEATHKNIGHT,,,BLOODELF,UNDEAD,BLOODELF,,,HORDE, YES,1669268910,1669269075,562,165,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1156,1207,51,1361,1325,1314,-11,1366,,Ctweezy,Sowocide,Suwushine,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,ALLIANCE, YES,1669269075,1669269271,617,196,,GOLD,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1213,1213,0,1402,1268,1308,40,1436,,Dracelym-Grobbulus,Qzsvkopfoe-Grobbulus,Flakked-Grobbulus,,,DEATHKNIGHT,MAGE,PALADIN,,,HUMAN,HUMAN,HUMAN,,,ALLIANCE, YES,1669269271,1669269476,562,205,,GREEN,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1210,1210,0,1373,1331,1348,17,1364,,Remdog-Earthfury,Bullsofwar-Earthfury,Oatie-Earthfury,,,DEATHKNIGHT,WARRIOR,PRIEST,,,ORC,TAUREN,UNDEAD,,,HORDE, YES,1669269477,1669269664,562,187,,GREEN,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1205,1239,34,1335,1375,1362,-13,1330,,Quagnardmx-Grobbulus,Redsippylock-Grobbulus,Tolarentcow-Grobbulus,,,SHAMAN,WARLOCK,DRUID,,,ORC,ORC,TAUREN,,,HORDE, YES,1669269664,1669269844,617,180,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1245,1285,40,1368,1130,1130,0,1504,,Gnowps-Grobbulus,Majinchown-Grobbulus,Majingassed-Grobbulus,,,PALADIN,PRIEST,HUNTER,,,HUMAN,DWARF,DWARF,,,ALLIANCE, YES,1669269844,1669270007,572,163,,GREEN,GREEN,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1288,1324,36,1419,1348,1338,-10,1437,,Aliè-Benediction,Arenaslave-Benediction,Blizrdsuport-Benediction,,,ROGUE,DRUID,PRIEST,,,NIGHTELF,NIGHTELF,HUMAN,,,ALLIANCE, YES,1669270007,1669270194,572,187,,GOLD,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1326,1360,34,1454,1387,1377,-10,1454,,Faulty-Eranikus,Felixdelao-Eranikus,ßlazen-Eranikus,,,PRIEST,WARLOCK,SHAMAN,,,HUMAN,HUMAN,DRAENEI,,,ALLIANCE, YES,1669270194,1669270455,572,261,,GOLD,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1361,1356,-5,1483,1473,1487,14,1491,,Baxterbb-Sulfuras,Kidneydatass-Sulfuras,Redvietnam-Sulfuras,,,PRIEST,ROGUE,SHAMAN,,,HUMAN,HUMAN,DRAENEI,,,ALLIANCE, YES,1669270455,1669270677,572,222,,GOLD,GOLD,Cope,Backwoods,Opsec,,,DEATHKNIGHT,WARRIOR,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1358,1389,31,1456,1278,1278,0,1512,,Bigdkcalon-Grobbulus,Blaqpriest-Grobbulus,Robbyrotten-Grobbulus,,,DEATHKNIGHT,PRIEST,SHAMAN,,,HUMAN,DWARF,DRAENEI,,,ALLIANCE, YES,1669270677,1669270889,562,212,,GREEN,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1390,1382,-8,1494,1421,1448,27,1520,,Samshelby-Sulfuras,Beamerr-Sulfuras,Iolunholy-Sulfuras,,,WARRIOR,DEATHKNIGHT,PALADIN,,,GNOME,HUMAN,HUMAN,,,ALLIANCE, YES,1669270890,1669271139,559,249,,GREEN,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1386,1377,-9,1470,1475,1488,13,1486,,Muffinn-Grobbulus,Wotson-Grobbulus,Bananabræd-Grobbulus,,,WARRIOR,PRIEST,DEATHKNIGHT,,,ORC,UNDEAD,ORC,,,HORDE, YES,1669271140,1669271423,562,283,,GREEN,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1378,1369,-9,1444,1454,1467,13,1469,,Cammyboi-Faerlina,Derpulez-Faerlina,Yinxzz-Faerlina,,,WARRIOR,SHAMAN,PALADIN,,,ORC,ORC,BLOODELF,,,HORDE, YES,1669271423,1669271702,617,279,,GOLD,GREEN,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1369,1357,-12,1420,1337,1356,19,1371,,Azory-Faerlina,Saiwong-Faerlina,Zygy-Faerlina,,,ROGUE,MAGE,PRIEST,,,BLOODELF,UNDEAD,BLOODELF,,,HORDE, YES,1669271702,1669271900,559,198,,GREEN,GOLD,Backwoods,Cope,Opsec,,,WARRIOR,DEATHKNIGHT,PALADIN,,,HUMAN,HUMAN,HUMAN,,,1357,1346,-11,1380,1408,1419,11,1378,,Smokebee-Grobbulus,Ctrldoom-Grobbulus,Niffler-Grobbulus,,,HUNTER,PALADIN,PRIEST,,,TROLL,BLOODELF,TROLL,,,HORDE,"
