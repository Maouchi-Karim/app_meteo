import numpy as np
import pandas as pd
import datetime as dt
from random import random, randint
from dataframe import df, temp_colonne
from datetime import datetime, timedelta
import meteostat as ms


def sigmoide(x):
    y = 1/(1+np.exp(-x))
    return y

def reLu(X):
    return np.maximum(0,X)


def reLu_prime(X):
    return (X > 0)
    


def forwardpass(M1, M2, M3, B1, B2, B3, X_test):
    Z1 = np.dot(X_test, M1) + B1
    A1 = reLu(Z1)

    Z2 = np.dot(A1, M2) + B2
    A2 = reLu(Z2)

    Z3 = np.dot(A2, M3) + B3
    return Z3


def cree_matrices():

    np.random.seed(8)

    M1 = np.random.randn(11, 32) * np.sqrt(2 / 11)
    M2 = np.random.randn(32, 16) * np.sqrt(2 / 32)
    M3 = np.random.randn(16,) * np.sqrt(2 / 16)

    """for i in range(11):
        for j in range(16):
            M1[i,j] = randint(-1, 1)*random()

    for i in range(16):
        for j in range(16):
            M2[i,j] = randint(-1, 1)*random()

    for i in range(16):
            M3[i] = randint(-1, 1)*random()"""


    B1 = np.random.randn(32) * np.sqrt(2/11)
    B2 = np.random.randn(16) * np.sqrt(2/32)
    B3 = np.random.randn() * np.sqrt(2/16)

    np.save('M1.npy',M1)
    np.save('M2.npy', M2)
    np.save('M3.npy', M3)

    np.save('B1.npy', B1)
    np.save('B2.npy', B2)
    np.save('B3.npy', B3)
     
    print("les matrices ont été créés !")

    return M1, M2, M3, B1, B2, B3




def entrainer(X, Y, M1, M2, M3, B1, B2, B3, alpha, nb_epochs):

    m = X.shape[0]

    courbe_loss = []


    for epoch in range (nb_epochs):
        
        Z1 = np.dot(X,M1) + B1
        A1 = reLu(Z1)

        Z2 = np.dot(A1, M2) + B2
        A2 = reLu(Z2)

        Z3 = np.dot(A2, M3) + B3

        """
        print("A2 shape:", A2.shape)
        print("M3 shape:", M3.shape)
        print("B3:", B3, type(B3))
        """

        erreurs = Z3 - Y

        MSE = 1/m * np.sum(erreurs**2)

        courbe_loss.append(MSE)


        #backward pass

        dZ3 = (2/m) * (Z3 - Y)
        dM3 = np.dot(A2.T , dZ3)
        dB3 = np.sum(dZ3)

        dA2 = np.outer(dZ3, M3)
        dZ2 = reLu_prime(Z2)*dA2
        dM2 = np.dot(A1.T , dZ2)
        dB2 = np.sum(dZ2, axis = 0)

        dA1 = np.dot(dZ2 , M2.T)
        dZ1 = reLu_prime(Z1)*dA1
        dM1 = np.dot(X.T , dZ1)
        dB1 = np.sum(dZ1, axis = 0)

        """
        print(dM1.shape, M1.shape)  # doivent être identiques : (11, 32)
        print(dM2.shape, M2.shape)  # (32, 16)
        print(dM3.shape, M3.shape)  # (16,)
        print(dB1.shape, B1.shape)  # (32,)
        print(dB2.shape, B2.shape)  # (16,)
        """

        M1 = M1 - alpha * dM1
        M2 = M2 - alpha * dM2
        M3 = M3 - alpha * dM3

        B1 = B1 - alpha * dB1
        B2 = B2 - alpha * dB2
        B3 = B3 - alpha * dB3
        print(epoch)
    

    return M1, M2, M3, B1, B2, B3, courbe_loss



def donnees_recentes():

    station = ms.stations.meta('07222')

    fin = datetime.now()
    debut = fin - timedelta(hours=48)

    ts = ms.hourly(station, debut, fin)
    df_recent = ts.fetch()

    derniere_ligne = df_recent.iloc[-1]  
    colonnes_manquantes = derniere_ligne[derniere_ligne.isna()].index.tolist()

    df_recent.ffill(inplace=True)
    derniere_ligne = df_recent.iloc[-1]

    avant_derniere_ligne = df_recent.iloc[-2]
    temp_pre = avant_derniere_ligne['temp']

    derniere_ligne['temp_pre'] = temp_pre
    
    return derniere_ligne, colonnes_manquantes




def preparer_ligne(ligne):

    stats = np.load('stats_normalisation.npy', allow_pickle=True).item()

    # temp à part
    temp_reelle = ligne['temp']

    # time
    t = pd.to_datetime(ligne.name)
    time_val = t.hour + t.day*24 + t.month*24*30
    time_cos = np.cos(time_val * 2*np.pi/9384)
    time_sin = np.sin(time_val * 2*np.pi/9384)

    
    # wdir
    wdir_cos = np.cos(ligne['wdir'] * 2*np.pi/360)
    wdir_sin = np.sin(ligne['wdir'] * 2*np.pi/360)

    #heure
    heure_colonne = pd.to_datetime(ligne.name)
    heure_val = heure_colonne.hour
    heure_cos = np.cos(heure_val * 2*np.pi/24)
    heure_sin = np.sin(heure_val * 2*np.pi/24)



    # normalisations
    pres_norm = (ligne['pres'] - stats['pres_mean']) / stats['pres_std']
    rhum_norm = (ligne['rhum'] - stats['rhum_mean']) / stats['rhum_std']
    prcp_norm = (ligne['prcp'] - stats['prcp_mean']) / stats['prcp_std']
    wspd_norm = (ligne['wspd'] - stats['wspd_mean']) / stats['wspd_std']
    wpgt_norm = (ligne['wpgt'] - stats['wpgt_mean']) / stats['wpgt_std']
    cldc_norm = (ligne['cldc'] - stats['cldc_mean']) / stats['cldc_std']
    coco_norm = (ligne['coco'] - stats['coco_mean']) / stats['coco_std']
    #tsun_norm = (ligne['tsun'] - stats['tsun_mean']) / stats['tsun_std']
    #temp_pre_norm = (ligne['temp_pre'] - stats['temp_pre_mean']) / stats['temp_pre_std']

    # reconstruction dans le bon ordre (identique à dataframe.py)
    ligne_finale = pd.Series({
        'time': time_cos,
        'time_sin': time_sin,
        'rhum': rhum_norm,
        'prcp': prcp_norm,
        'wdir': wdir_cos,
        'wdir_colonne_sin': wdir_sin,
        'wspd': wspd_norm,
        'wpgt': wpgt_norm,
        'pres': pres_norm,
        'cldc': cldc_norm,
        'coco': coco_norm,
        #'temp_pre':temp_pre_norm,
        #'heure_cos': heure_cos,
        #'heure_sin': heure_sin,
        #'tsun': tsun_norm,
    })

    return ligne_finale.values.reshape(1, -1), temp_reelle


def predire(ligne_preparee, M1, M2, M3, B1, B2, B3, mu_Y, sigma_Y):
    Z3 = forwardpass(M1, M2, M3, B1, B2, B3, ligne_preparee)
    temp_predite = Z3 * sigma_Y + mu_Y
    return temp_predite.item()  
    