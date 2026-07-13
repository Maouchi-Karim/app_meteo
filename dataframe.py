import numpy as np
import pandas as pd
import datetime as dt
from random import random, randint



#ici je forme le dataframe à partir du dataset et je retir la colonne pres que je conserve dans pres_colonne
df = pd.read_csv('dataframe.csv')

#visualisation des données manquantes 

valeur_manquantes = df.isna().sum()
print("\n\n\n Nombre de valeurs manquantes par colonne\n\n", valeur_manquantes)


temp_colonne = df['temp']
df = df.drop('temp', axis=1)
df = df.drop('snwd', axis=1)

#df['temp_pre'] = temp_colonne.shift(1)

stats = {
    'pres_mean': np.mean(df['pres']), 'pres_std': np.std(df['pres']),
    'rhum_mean': np.mean(df['rhum']), 'rhum_std': np.std(df['rhum']),
    'prcp_mean': np.mean(df['prcp']), 'prcp_std': np.std(df['prcp']),
    'wspd_mean': np.mean(df['wspd']), 'wspd_std': np.std(df['wspd']),
    'wpgt_mean': np.mean(df['wpgt']), 'wpgt_std': np.std(df['wpgt']),
    'cldc_mean': np.mean(df['cldc']), 'cldc_std': np.std(df['cldc']),
    'coco_mean': np.mean(df['coco']), 'coco_std': np.std(df['coco']),
    'tsun_mean': np.mean(df['tsun']), 'tsun_std': np.std(df['tsun']),
    #'temp_pre_mean': np.mean(df['temp_pre']), 'temp_pre_std': np.std(df['temp_pre']),
}
np.save('stats_normalisation.npy', stats)
print("stats_normalisation.npy sauvegardé !")

#ici je mets en forme la colonne des dates pour en faire des floats comprient entre -1 et 1, et j'utilise un cos pour que le 1 jan et le 31 dec ne soient pas opposées en valeur
date_colonne = df['time']
date_colonne = pd.to_datetime(date_colonne).dt.hour + pd.to_datetime(date_colonne).dt.day*24 + pd.to_datetime(date_colonne).dt.month*24*30
date_colonne_cos = np.cos(date_colonne.astype(float)*2*np.pi/9384)
date_colonne_sin = np.sin(date_colonne.astype(float)*2*np.pi/9384)

df['time'] = date_colonne_cos
df.insert(1, 'time_sin', date_colonne_sin)


"""df = df.drop('time', axis=1)
df.insert(0, 'time', date_colonne)"""


#pour le sens sur vent on fait pareil que pour la date 
wdir_colonne = df['wdir']
wdir_colonne_cos = np.cos(wdir_colonne.astype(float)*2*np.pi/360)
wdir_colonne_sin = np.sin(wdir_colonne.astype(float)*2*np.pi/360)
df['wdir'] = wdir_colonne_cos
df.insert(5, 'wdir_colonne_sin', wdir_colonne_sin)

"""
df = df.drop('wdir', axis=1)
df.insert(5, 'wdir', wdir_colonne)"""


pres_colonne = df['pres'].astype(float) + 273.15
pres_colonne = (pres_colonne - np.mean(pres_colonne))/np.std(pres_colonne)
df['pres'] = pres_colonne


rhum_colonne = df['rhum'].astype(float)
rhum_colonne = (rhum_colonne - np.mean(rhum_colonne))/np.std(rhum_colonne)
df['rhum'] = rhum_colonne

prcp_colonne = df['prcp'].astype(float)
prcp_colonne = (prcp_colonne - np.mean(prcp_colonne))/np.std(prcp_colonne)
df['prcp'] = prcp_colonne


wspd_colonne = df['wspd'].astype(float)
wspd_colonne = (wspd_colonne - np.mean(wspd_colonne))/np.std(wspd_colonne)
df['wspd'] = wspd_colonne

wpgt_colonne = df['wpgt'].astype(float)
wpgt_colonne = (wpgt_colonne - np.mean(wpgt_colonne))/np.std(wpgt_colonne)
df['wpgt'] = wpgt_colonne


cldc_colonne = df['cldc'].astype(float)
cldc_colonne = (cldc_colonne - np.mean(cldc_colonne))/np.std(cldc_colonne)
df['cldc'] = cldc_colonne

coco_colonne = df['coco'].astype(float)
coco_colonne = (coco_colonne - np.mean(coco_colonne))/np.std(coco_colonne)
df['coco'] = coco_colonne

"""temp_pre_colonne = df['temp_pre'].astype(float)
temp_pre_colonne = (temp_pre_colonne - np.mean(temp_pre_colonne))/np.std(temp_pre_colonne)
df['temp_pre'] = temp_pre_colonne"""

heure_colonne = pd.to_datetime(df['time']).dt.hour
heure_cos = np.cos(heure_colonne * 2*np.pi/24)
heure_sin = np.sin(heure_colonne * 2*np.pi/24)
df['heure_cos'] = heure_cos
df['heure_sin'] = heure_sin

tsun_colonne = df['tsun'].astype(float)
tsun_colonne = (tsun_colonne - np.mean(tsun_colonne))/np.std(tsun_colonne)
df['tsun'] = tsun_colonne

#df = df.drop('tsun', axis=1)


df.interpolate(inplace=True)
df.bfill(inplace=True)
df.ffill(inplace=True)

"""np.save('df.npy', df)"""

valeur_manquantes = df.isna().sum()
print("\n\n\n Nombre de valeurs manquantes par colonne\n\n", valeur_manquantes)

print(type(temp_colonne))
print(temp_colonne.shape)

print(df.iloc[1:10])

print(np.shape(df))