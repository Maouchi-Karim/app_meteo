from flask import Flask, render_template, jsonify
import numpy as np
import os
from modele import forwardpass, entrainer, cree_matrices, donnees_recentes, preparer_ligne, predire
from dataframe import df, temp_colonne

app = Flask(__name__)

# --- Préparation des données ---

alpha = 0.01
nb_epochs = 20
lines = len(df)
lines_train = int(lines*0.8)

mu_Y = np.mean(temp_colonne.head(lines_train))
sigma_Y = np.std(temp_colonne.head(lines_train))
Y_test_original = temp_colonne.iloc[lines_train:].values
X = df.head(lines_train).values
Y = temp_colonne.head(lines_train).values
Y = (Y - mu_Y) / sigma_Y
X_test = df.iloc[lines_train:].values

# --- Chargement ou création des matrices ---
if os.path.exists("M1.npy"):
    M1 = np.load("M1.npy")
    M2 = np.load("M2.npy")
    M3 = np.load("M3.npy")
    B1 = np.load("B1.npy")
    B2 = np.load("B2.npy")
    B3 = np.load("B3.npy")
else:
    M1, M2, M3, B1, B2, B3 = cree_matrices()

# --- Routes Flask ---
@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/entrainer')
def entrainement():
    global M1, M2, M3, B1, B2, B3

    M1, M2, M3, B1, B2, B3, courbe_loss = entrainer(X, Y, M1, M2, M3, B1, B2, B3, alpha, nb_epochs)

    np.save("M1.npy", M1)
    np.save("M2.npy", M2)
    np.save("M3.npy", M3)
    np.save("B1.npy", B1)
    np.save("B2.npy", B2)
    np.save("B3.npy", B3)

    return jsonify({"courbe_loss": courbe_loss})


@app.route('/import_data')
def import_data():
    derniere_ligne, colonnes_manquantes = donnees_recentes()
    derniere_ligne_prepared, temp_reelle = preparer_ligne(derniere_ligne)

    return jsonify({
        "message": "Les données ont bien été collectées",
        "derniere_ligne": derniere_ligne.to_dict() if hasattr(derniere_ligne, 'to_dict') else derniere_ligne,
        "colonnes_manquantes": list(colonnes_manquantes)
    })

@app.route('/predire')
def prediction():
    derniere_ligne, colonnes_manquantes = donnees_recentes()
    ligne_preparee, temp_reelle = preparer_ligne(derniere_ligne)
    
    temp_predite = predire(ligne_preparee, M1, M2, M3, B1, B2, B3, mu_Y, sigma_Y)
    
    return jsonify({
        "temp_predite": float(temp_predite),
        "temp_reelle": float(temp_reelle)
    })

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))