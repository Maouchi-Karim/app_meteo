function lancerEntrainement() {
    fetch('/entrainer')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('graphique_loss').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({length: data.courbe_loss.length}, (_, i) => i),
                    datasets: [{
                        label: 'Loss',
                        data: data.courbe_loss,
                        borderColor: 'blue',
                        fill: false
                    }]
                },
                options: {
                    responsive: false,
                    scales: {
                        y: {
                        type: 'logarithmic'
                        }
                    }
                }
            });
        });
}

function donnees(){
    fetch('/import_data')
        .then(response => response.json())
        .then(data => {
            const div = document.getElementById('resultat_donnees');
            
            let html = `<p>${data.message}</p>`;
            html += '<ul>';
            for (const [cle, valeur] of Object.entries(data.derniere_ligne)) {
                html += `<li>${cle} : ${valeur}</li>`;
            }
            html += '</ul>';

            if (data.colonnes_manquantes.length > 0) {
                html += `<p>Colonnes manquantes complétées : ${data.colonnes_manquantes.join(', ')}</p>`;
            } else {
                html += `<p>Aucune donnée manquante.</p>`;
            }

            div.innerHTML = html;
        });
}


function lancerPrediction(){
    fetch('/predire')
        .then(response => response.json())
        .then(data => {
            const div = document.getElementById('resultat_prediction');
            div.innerHTML = `<p>Température prédite : ${data.temp_predite.toFixed(2)} °C</p>
                              <p>Température réelle (dernière donnée connue) : ${data.temp_reelle.toFixed(2)} °C</p>`;
        });
}