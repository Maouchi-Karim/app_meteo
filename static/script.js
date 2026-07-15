function setLoading(btnId, spinId, statusId, loading, msg) {
    document.getElementById(btnId).disabled = loading;
    document.getElementById(spinId).classList.toggle('active', loading);
    document.getElementById(statusId).textContent = msg || '';
}

function lancerEntrainement() {
    setLoading('btn-train', 'spin-train', 'status-train', true, 'Entraînement en cours…');

    fetch('/entrainer')
        .then(response => response.json())
        .then(data => {
            const nb = data.courbe_loss.length;
            const last = data.courbe_loss[nb - 1].toFixed(4);
            setLoading('btn-train', 'spin-train', 'status-train', false,
                `Terminé · ${nb} epochs · Loss finale : ${last}`);

            const wrapper = document.getElementById('loss-wrapper');
            wrapper.classList.add('visible');

            const ctx = document.getElementById('graphique_loss').getContext('2d');
            if (window._lossChart) window._lossChart.destroy();

            window._lossChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({ length: nb }, (_, i) => i + 1),
                    datasets: [{
                        label: 'Loss (MSE)',
                        data: data.courbe_loss,
                        borderColor: '#378ADD',
                        borderWidth: 1.5,
                        pointRadius: 0,
                        fill: false,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: {
                            ticks: { maxTicksLimit: 6, color: '#9d9d98', font: { size: 11 } },
                            grid: { display: false }
                        },
                        y: {
                            ticks: { color: '#9d9d98', font: { size: 11 } },
                            grid: { color: 'rgba(136,135,128,0.12)' }
                        }
                    }
                }
            });
        })
        .catch(() => {
            setLoading('btn-train', 'spin-train', 'status-train', false,
                'Erreur lors de l\'entraînement.');
        });
}

function donnees() {
    setLoading('btn-import', 'spin-import', 'status-import', true, 'Récupération en cours…');

    fetch('/import_data')
        .then(response => response.json())
        .then(data => {
            setLoading('btn-import', 'spin-import', 'status-import', false, data.message);

            const div = document.getElementById('resultat_donnees');
            div.classList.add('visible');

            let html = '<div class="data-grid">';
            for (const [cle, valeur] of Object.entries(data.derniere_ligne)) {
                const affichage = typeof valeur === 'number' ? valeur.toFixed(2) : valeur;
                html += `
                    <div class="data-item">
                        <div class="data-label">${cle}</div>
                        <div class="data-value">${affichage}</div>
                    </div>`;
            }
            html += '</div>';

            if (data.colonnes_manquantes && data.colonnes_manquantes.length > 0) {
                const cols = data.colonnes_manquantes.join(', ');
                html += `
                    <div class="warning-strip">
                        <i class="ti ti-alert-triangle" aria-hidden="true"></i>
                        <span>Données manquantes complétées par interpolation : <strong>${cols}</strong></span>
                    </div>`;
            }

            div.innerHTML = html;
        })
        .catch(() => {
            setLoading('btn-import', 'spin-import', 'status-import', false,
                'Erreur lors de l\'import.');
        });
}

function lancerPrediction() {
    setLoading('btn-predict', 'spin-predict', 'status-predict', true, 'Calcul en cours…');

    fetch('/predire')
        .then(response => response.json())
        .then(data => {
            setLoading('btn-predict', 'spin-predict', 'status-predict', false, '');

            const div = document.getElementById('resultat_prediction');
            div.classList.add('visible');

            const ecart = Math.abs(data.temp_predite - data.temp_reelle);
            const bonne = ecart < 3;
            const classeEcart = bonne ? 'good' : 'bad';

            div.innerHTML = `
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">Température prédite</div>
                        <div class="metric-value">${data.temp_predite.toFixed(1)} °C</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Température réelle</div>
                        <div class="metric-value">${data.temp_reelle.toFixed(1)} °C</div>
                    </div>
                    <div class="metric full">
                        <div class="metric-label">Écart absolu</div>
                        <div class="metric-value ${classeEcart}">${ecart.toFixed(1)} °C</div>
                    </div>
                </div>`;
        })
        .catch(() => {
            setLoading('btn-predict', 'spin-predict', 'status-predict', false,
                'Erreur lors de la prédiction.');
        });
}














/*

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


*/