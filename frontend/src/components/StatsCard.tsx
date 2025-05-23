import React from 'react';
import './StatsCard.css';

interface StatsCardProps {
  title: string;
  value: number;
  unit: string;
  icon: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, unit, icon }) => {
  return (
    <div className="stats-card">
      <div className="stats-card-icon">
        <i className={icon}></i>
      </div>
      <div className="stats-card-content">
        <h3 className="stats-card-title">{title}</h3>
        <p className="stats-card-value">
          {value} <span className="stats-card-unit">{unit}</span>
        </p>
      </div>
    </div>
  );
};

export default StatsCard; 