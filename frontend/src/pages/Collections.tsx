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
  CardContent,
  Tabs,
  Tab
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  LocalShipping as TruckIcon,
  CheckCircle as CompletedIcon,
  Schedule as ScheduledIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';

interface Collection {
  id: number;
  date: string;
  time: string;
  zone: string;
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  driver: string;
  vehicle: string;
  bins: number;
  weight: number;
}

const mockCollections: Collection[] = [
  {
    id: 1,
    date: '2024-03-20',
    time: '08:00',
    zone: 'Zone A',
    status: 'completed',
    driver: 'Jean Dupont',
    vehicle: 'Camion-001',
    bins: 8,
    weight: 450
  },
  {
    id: 2,
    date: '2024-03-20',
    time: '10:30',
    zone: 'Zone B',
    status: 'in_progress',
    driver: 'Marie Martin',
    vehicle: 'Camion-002',
    bins: 5,
    weight: 280
  },
  {
    id: 3,
    date: '2024-03-20',
    time: '14:00',
    zone: 'Zone C',
    status: 'scheduled',
    driver: 'Pierre Durand',
    vehicle: 'Camion-003',
    bins: 3,
    weight: 0
  }
];

const getStatusColor = (status: Collection['status']) => {
  switch (status) {
    case 'completed':
      return 'success';
    case 'in_progress':
      return 'info';
    case 'scheduled':
      return 'warning';
    case 'cancelled':
      return 'error';
    default:
      return 'default';
  }
};

const getStatusIcon = (status: Collection['status']) => {
  switch (status) {
    case 'completed':
      return <CompletedIcon />;
    case 'in_progress':
      return <TruckIcon />;
    case 'scheduled':
      return <ScheduledIcon />;
    case 'cancelled':
      return <ErrorIcon />;
    default:
      return <InfoIcon />;
  }
};

const CollectionStats = ({ collections }: { collections: Collection[] }) => {
  const completed = collections.filter(c => c.status === 'completed').length;
  const inProgress = collections.filter(c => c.status === 'in_progress').length;
  const scheduled = collections.filter(c => c.status === 'scheduled').length;
  const totalWeight = collections.reduce((acc, c) => acc + c.weight, 0);

  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' }, gap: 3, mb: 3 }}>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Collectes complétées
            </Typography>
            <Typography variant="h4">
              {completed}
            </Typography>
          </CardContent>
        </Card>
      </Box>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              En cours
            </Typography>
            <Typography variant="h4">
              {inProgress}
            </Typography>
          </CardContent>
        </Card>
      </Box>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Planifiées
            </Typography>
            <Typography variant="h4">
              {scheduled}
            </Typography>
          </CardContent>
        </Card>
      </Box>
      <Box>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Poids total (kg)
            </Typography>
            <Typography variant="h4">
              {totalWeight}
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

const Collections = () => {
  const [collections, setCollections] = useState<Collection[]>(mockCollections);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gestion des collectes
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ mr: 1 }}
          >
            Planifier
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
          >
            Actualiser
          </Button>
        </Box>
      </Box>

      <CollectionStats collections={collections} />

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Toutes les collectes" />
          <Tab label="En cours" />
          <Tab label="Planifiées" />
          <Tab label="Complétées" />
        </Tabs>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Heure</TableCell>
              <TableCell>Zone</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Chauffeur</TableCell>
              <TableCell>Véhicule</TableCell>
              <TableCell>Poubelles</TableCell>
              <TableCell>Poids (kg)</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {collections.map((collection) => (
              <TableRow key={collection.id}>
                <TableCell>{collection.id}</TableCell>
                <TableCell>{collection.date}</TableCell>
                <TableCell>{collection.time}</TableCell>
                <TableCell>{collection.zone}</TableCell>
                <TableCell>
                  <Chip
                    icon={getStatusIcon(collection.status)}
                    label={collection.status}
                    color={getStatusColor(collection.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{collection.driver}</TableCell>
                <TableCell>{collection.vehicle}</TableCell>
                <TableCell>{collection.bins}</TableCell>
                <TableCell>{collection.weight}</TableCell>
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

export default Collections; 