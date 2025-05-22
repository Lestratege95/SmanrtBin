import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Navigation = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          SmartBin
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" component={RouterLink} to="/">
            Accueil
          </Button>
          <Button color="inherit" component={RouterLink} to="/bins">
            Poubelles
          </Button>
          <Button color="inherit" component={RouterLink} to="/zones">
            Zones
          </Button>
          <Button color="inherit" component={RouterLink} to="/collections">
            Collectes
          </Button>
          <Button color="inherit" component={RouterLink} to="/alerts">
            Alertes
          </Button>
          <Button color="inherit" component={RouterLink} to="/tri-centers">
            Centres de tri
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation; 