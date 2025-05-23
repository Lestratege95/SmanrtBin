import React from 'react';
import Navbar from '../components/Navbar';
import './SensorsPage.css';

interface Sensor {
  id: number;
  name: string;
  type: string;
  status: 'active' | 'inactive' | 'maintenance';
  lastReading: string;
  batteryLevel: number;
}

const SensorsPage: React.FC = () => {
  const sensors: Sensor[] = [
    {
      id: 1,
      name: "Capteur de Niveau",
      type: "Ultrasonique",
      status: "active",
      lastReading: "75%",
      batteryLevel: 85
    },
    {
      id: 2,
      name: "Capteur de Température",
      type: "Thermique",
      status: "active",
      lastReading: "23°C",
      batteryLevel: 92
    },
    {
      id: 3,
      name: "Capteur de Qualité",
      type: "Air",
      status: "maintenance",
      lastReading: "N/A",
      batteryLevel: 45
    }
  ];

  const getStatusColor = (status: Sensor['status']) => {
    switch (status) {
      case 'active':
        return '#2ecc71';
      case 'inactive':
        return '#e74c3c';
      case 'maintenance':
        return '#f1c40f';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className="sensors-page">
      <Navbar />
      <div className="sensors-content">
        <h1 className="sensors-title">État des Capteurs</h1>
        
        <div className="sensors-grid">
          {sensors.map((sensor) => (
            <div key={sensor.id} className="sensor-card">
              <div className="sensor-header">
                <h3>{sensor.name}</h3>
                <span
                  className="sensor-status"
                  style={{ backgroundColor: getStatusColor(sensor.status) }}
                >
                  {sensor.status}
                </span>
              </div>
              
              <div className="sensor-details">
                <p><strong>Type:</strong> {sensor.type}</p>
                <p><strong>Dernière lecture:</strong> {sensor.lastReading}</p>
                <div className="battery-indicator">
                  <strong>Batterie:</strong>
                  <div className="battery-bar">
                    <div 
                      className="battery-level"
                      style={{ width: `${sensor.batteryLevel}%` }}
                    ></div>
                  </div>
                  <span>{sensor.batteryLevel}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SensorsPage; 