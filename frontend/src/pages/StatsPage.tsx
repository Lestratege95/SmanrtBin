import React from 'react';
import Navbar from '../components/Navbar';
import StatsCard from '../components/StatsCard';
import './StatsPage.css';

const StatsPage: React.FC = () => {
  return (
    <div className="stats-page">
      <Navbar />
      <div className="stats-content">
        <h1 className="stats-title">Statistiques Détaillées</h1>
        
        <div className="stats-overview">
          <StatsCard 
            title="Total des Poubelles"
            value={25}
            unit="unités"
            icon="fas fa-trash"
          />
          <StatsCard 
            title="Remplissage Moyen"
            value={68}
            unit="%"
            icon="fas fa-chart-pie"
          />
          <StatsCard 
            title="Collectes Hebdo"
            value={42}
            unit="fois"
            icon="fas fa-truck"
          />
          <StatsCard 
            title="Économies CO2"
            value={1250}
            unit="kg"
            icon="fas fa-leaf"
          />
        </div>

        <div className="stats-details">
          <div className="stats-chart">
            <h2>Évolution du Remplissage</h2>
            <div className="chart-placeholder">
              {/* Ici, vous pourrez intégrer un composant de graphique comme Chart.js */}
              <p>Graphique d'évolution du remplissage</p>
            </div>
          </div>

          <div className="stats-chart">
            <h2>Répartition par Zone</h2>
            <div className="chart-placeholder">
              {/* Ici, vous pourrez intégrer un composant de graphique comme Chart.js */}
              <p>Graphique de répartition par zone</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsPage; 