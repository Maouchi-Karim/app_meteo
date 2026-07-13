from datetime import datetime
import meteostat as ms

ms.config.block_large_requests = False
station = ms.stations.meta('07157')

debut = datetime(2015, 1, 1, 0, 0)
fin = datetime(2025, 12, 31, 23, 0)

ts = ms.hourly(station, debut, fin) #timezone mis à None, je me demande comment sont gérées les changements d'heures été/hiver si on met UTC+1 ...
df = ts.fetch()

#là, normalement, le datafram est crée et remplie

with open('dataframe.csv', 'w') as fichier :
    df.to_csv('dataframe.csv')

