import React from 'react';
import './BinList.css';

interface Bin {
  id: number;
  location: string;
  fillLevel: number;
  lastUpdated: string;
  status: 'active' | 'maintenance' | 'full';
}

interface BinListProps {
  bins: Bin[];
}

const BinList: React.FC<BinListProps> = ({ bins }) => {
  const getStatusColor = (status: Bin['status']) => {
    switch (status) {
      case 'active':
        return '#2ecc71';
      case 'maintenance':
        return '#f1c40f';
      case 'full':
        return '#e74c3c';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className="bin-list">
      <h2 className="bin-list-title">Liste des Poubelles</h2>
      <div className="bin-list-container">
        {bins.map((bin) => (
          <div key={bin.id} className="bin-card">
            <div className="bin-header">
              <h3>Poubelle #{bin.id}</h3>
              <span
                className="bin-status"
                style={{ backgroundColor: getStatusColor(bin.status) }}
              >
                {bin.status}
              </span>
            </div>
            <div className="bin-details">
              <p>
                <strong>Localisation:</strong> {bin.location}
              </p>
              <p>
                <strong>Niveau de remplissage:</strong> {bin.fillLevel}%
              </p>
              <p>
                <strong>Dernière mise à jour:</strong> {bin.lastUpdated}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BinList; 