import React, { useState } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Button,
  IconButton,
  Chip,
  Grid,
  Card,
  CardContent
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  LocationOn as LocationIcon
} from '@mui/icons-material';

interface Zone {
  id: number;
  name: string;
  description: string;
  status: 'active' | 'inactive';
  binCount: number;
  lastCollection: string;
  coordinates: string;
}

const mockZones: Zone[] = [
  {
    id: 1,
    name: 'Zone A',
    description: 'Centre-ville',
    status: 'active',
    binCount: 8,
    lastCollection: '2024-03-20',
    coordinates: '48.8566, 2.3522'
  },
  {
    id: 2,
    name: 'Zone B',
    description: 'Quartier résidentiel',
    status: 'active',
    binCount: 5,
    lastCollection: '2024-03-19',
    coordinates: '48.8606, 2.3376'
  },
  {
    id: 3,
    name: 'Zone C',
    description: 'Zone commerciale',
    status: 'inactive',
    binCount: 3,
    lastCollection: '2024-03-18',
    coordinates: '48.8706, 2.3476'
  }
];

const getStatusColor = (status: Zone['status']) => {
  return status === 'active' ? 'success' : 'error';
};

const ZoneStats = ({ zones }: { zones: Zone[] }) => {
  const totalBins = zones.reduce((acc, zone) => acc + zone.binCount, 0);
  const activeZones = zones.filter(zone => zone.status === 'active').length;

  return (
    <Box sx={{ 
      display: 'grid', 
      gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' }, 
      gap: 3,
      mb: 3 
    }}>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Zones totales
            </Typography>
            <Typography variant="h4">
              {zones.length}
            </Typography>
          </CardContent>
        </Card>
      </Box>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Zones actives
            </Typography>
            <Typography variant="h4">
              {activeZones}
            </Typography>
          </CardContent>
        </Card>
      </Box>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Poubelles totales
            </Typography>
            <Typography variant="h4">
              {totalBins}
            </Typography>
          </CardContent>
        </Card>
      </Box>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Moyenne par zone
            </Typography>
            <Typography variant="h4">
              {(totalBins / zones.length).toFixed(1)}
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

const Zones = () => {
  const [zones, setZones] = useState<Zone[]>(mockZones);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gestion des zones
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ mr: 1 }}
          >
            Ajouter
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
          >
            Actualiser
          </Button>
        </Box>
      </Box>

      <ZoneStats zones={zones} />

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nom</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Nombre de poubelles</TableCell>
              <TableCell>Dernière collecte</TableCell>
              <TableCell>Coordonnées</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {zones.map((zone) => (
              <TableRow key={zone.id}>
                <TableCell>{zone.id}</TableCell>
                <TableCell>{zone.name}</TableCell>
                <TableCell>{zone.description}</TableCell>
                <TableCell>
                  <Chip
                    label={zone.status}
                    color={getStatusColor(zone.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{zone.binCount}</TableCell>
                <TableCell>{zone.lastCollection}</TableCell>
                <TableCell>
                  <IconButton size="small" color="primary">
                    <LocationIcon />
                  </IconButton>
                  {zone.coordinates}
                </TableCell>
                <TableCell>
                  <IconButton size="small" color="primary">
                    <EditIcon />
                  </IconButton>
                  <IconButton size="small" color="error">
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Zones; 