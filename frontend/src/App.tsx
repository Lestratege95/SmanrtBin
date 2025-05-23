import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Container } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Bins from './pages/Bins';
import Zones from './pages/Zones';
import Collections from './pages/Collections';
import Alerts from './pages/Alerts';
import TriCenters from './pages/TriCenters';
import HomePage from './pages/HomePage';
import StatsPage from './pages/StatsPage';
import SensorsPage from './pages/SensorsPage';
import './App.css';

// Création du thème
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navigation />
        <Container sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/statistiques" element={<StatsPage />} />
            <Route path="/capteurs" element={<SensorsPage />} />
            <Route path="/bins" element={<Bins />} />
            <Route path="/zones" element={<Zones />} />
            <Route path="/collections" element={<Collections />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/tri-centers" element={<TriCenters />} />
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  );
};

export default App;
