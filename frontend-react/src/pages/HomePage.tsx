import React from 'react';
import Navbar from '../components/Navbar';
import StatsCard from '../components/StatsCard';
import BinList from '../components/BinList';
import './HomePage.css';

const HomePage: React.FC = () => {
  // Données de démonstration
  const bins = [
    {
      id: 1,
      location: "Zone A - Entrée principale",
      fillLevel: 75,
      lastUpdated: "2024-03-20 14:30",
      status: "active"
    },
    {
      id: 2,
      location: "Zone B - Cafétéria",
      fillLevel: 90,
      lastUpdated: "2024-03-20 14:25",
      status: "full"
    },
    {
      id: 3,
      location: "Zone C - Parking",
      fillLevel: 45,
      lastUpdated: "2024-03-20 14:20",
      status: "active"
    }
  ];

  return (
    <div className="home-page">
      <Navbar />
      <div className="home-content">
        <div className="stats-section">
          <StatsCard 
            title="Poubelles Actives"
            value={15}
            unit="unités"
            icon="fas fa-trash"
          />
          <StatsCard 
            title="Niveau Moyen"
            value={65}
            unit="%"
            icon="fas fa-chart-line"
          />
          <StatsCard 
            title="Alertes"
            value={3}
            unit="unités"
            icon="fas fa-exclamation-triangle"
          />
        </div>
        <BinList bins={bins} />
      </div>
    </div>
  );
};

export default HomePage; 