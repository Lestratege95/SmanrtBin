import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
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
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Poubelles actives" 
            value="24" 
            icon={<DeleteIcon fontSize="large" />} 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Zones couvertes" 
            value="8" 
            icon={<LocationIcon fontSize="large" />} 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Alertes en cours" 
            value="3" 
            icon={<WarningIcon fontSize="large" />} 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Collectes aujourd'hui" 
            value="12" 
            icon={<ShippingIcon fontSize="large" />} 
          />
        </Grid>
      </Grid>

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