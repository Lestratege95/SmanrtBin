import React from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { 
  Delete as DeleteIcon,
  LocationOn as LocationIcon,
  Warning as WarningIcon,
  LocalShipping as ShippingIcon
} from '@mui/icons-material';

const StatCard = ({ title, value, icon }: { title: string; value: string; icon: React.ReactNode }) => (
  <Paper sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
    <Box sx={{ color: 'primary.main' }}>{icon}</Box>
    <Box>
      <Typography variant="h6" component="div">
        {value}
      </Typography>
      <Typography color="text.secondary">
        {title}
      </Typography>
    </Box>
  </Paper>
);

const Home = () => {
  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Tableau de bord
      </Typography>
      
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' }, 
        gap: 3 
      }}>
        <Box>
          <StatCard 
            title="Poubelles actives" 
            value="24" 
            icon={<DeleteIcon fontSize="large" />} 
          />
        </Box>
        <Box>
          <StatCard 
            title="Zones couvertes" 
            value="8" 
            icon={<LocationIcon fontSize="large" />} 
          />
        </Box>
        <Box>
          <StatCard 
            title="Alertes en cours" 
            value="3" 
            icon={<WarningIcon fontSize="large" />} 
          />
        </Box>
        <Box>
          <StatCard 
            title="Collectes aujourd'hui" 
            value="12" 
            icon={<ShippingIcon fontSize="large" />} 
          />
        </Box>
      </Box>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Activité récente
        </Typography>
        <Paper sx={{ p: 2 }}>
          <Typography color="text.secondary">
            Aucune activité récente à afficher
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default Home; 