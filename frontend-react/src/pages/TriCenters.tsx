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
  Tab,
  LinearProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  Factory as FactoryIcon,
  TrendingUp as TrendingUpIcon,
  Recycling as RecyclingIcon,
  LocalShipping as ShippingIcon
} from '@mui/icons-material';

interface TriCenter {
  id: number;
  name: string;
  location: string;
  status: 'active' | 'maintenance' | 'inactive';
  capacity: number;
  currentLoad: number;
  dailyProcessed: number;
  efficiency: number;
  lastUpdate: string;
}

const mockTriCenters: TriCenter[] = [
  {
    id: 1,
    name: 'Centre de Tri Nord',
    location: 'Zone Industrielle Nord',
    status: 'active',
    capacity: 1000,
    currentLoad: 750,
    dailyProcessed: 450,
    efficiency: 85,
    lastUpdate: '2024-03-20 10:30'
  },
  {
    id: 2,
    name: 'Centre de Tri Sud',
    location: 'Zone Industrielle Sud',
    status: 'maintenance',
    capacity: 800,
    currentLoad: 200,
    dailyProcessed: 320,
    efficiency: 78,
    lastUpdate: '2024-03-20 09:15'
  },
  {
    id: 3,
    name: 'Centre de Tri Est',
    location: 'Zone Industrielle Est',
    status: 'active',
    capacity: 1200,
    currentLoad: 950,
    dailyProcessed: 580,
    efficiency: 92,
    lastUpdate: '2024-03-20 11:00'
  }
];

const getStatusColor = (status: TriCenter['status']) => {
  switch (status) {
    case 'active':
      return 'success';
    case 'maintenance':
      return 'warning';
    case 'inactive':
      return 'error';
    default:
      return 'default';
  }
};

const getEfficiencyColor = (efficiency: number) => {
  if (efficiency >= 90) return 'success';
  if (efficiency >= 75) return 'info';
  if (efficiency >= 60) return 'warning';
  return 'error';
};

const TriCenterStats = ({ centers }: { centers: TriCenter[] }) => {
  const totalCapacity = centers.reduce((acc, center) => acc + center.capacity, 0);
  const totalCurrentLoad = centers.reduce((acc, center) => acc + center.currentLoad, 0);
  const totalDailyProcessed = centers.reduce((acc, center) => acc + center.dailyProcessed, 0);
  const averageEfficiency = centers.reduce((acc, center) => acc + center.efficiency, 0) / centers.length;

  return (
    <Grid container spacing={3} sx={{ mb: 3 }}>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Capacité totale
            </Typography>
            <Typography variant="h4">
              {totalCapacity} t
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Charge actuelle
            </Typography>
            <Typography variant="h4">
              {totalCurrentLoad} t
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Traité aujourd'hui
            </Typography>
            <Typography variant="h4">
              {totalDailyProcessed} t
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <Card>
          <CardContent>
            <Typography color="text.secondary" gutterBottom>
              Efficacité moyenne
            </Typography>
            <Typography variant="h4" color={getEfficiencyColor(averageEfficiency)}>
              {averageEfficiency.toFixed(1)}%
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

const TriCenters = () => {
  const [centers, setCenters] = useState<TriCenter[]>(mockTriCenters);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Centres de tri
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ mr: 1 }}
          >
            Nouveau centre
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
          >
            Actualiser
          </Button>
        </Box>
      </Box>

      <TriCenterStats centers={centers} />

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Tous les centres" />
          <Tab label="Actifs" />
          <Tab label="En maintenance" />
        </Tabs>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nom</TableCell>
              <TableCell>Emplacement</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Capacité</TableCell>
              <TableCell>Charge actuelle</TableCell>
              <TableCell>Traîté aujourd'hui</TableCell>
              <TableCell>Efficacité</TableCell>
              <TableCell>Dernière mise à jour</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {centers.map((center) => (
              <TableRow key={center.id}>
                <TableCell>{center.id}</TableCell>
                <TableCell>{center.name}</TableCell>
                <TableCell>{center.location}</TableCell>
                <TableCell>
                  <Chip
                    label={center.status}
                    color={getStatusColor(center.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{center.capacity} t</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: '100%', mr: 1 }}>
                      <LinearProgress 
                        variant="determinate" 
                        value={(center.currentLoad / center.capacity) * 100}
                        color={center.currentLoad > center.capacity * 0.9 ? 'error' : 'primary'}
                      />
                    </Box>
                    <Box sx={{ minWidth: 35 }}>
                      <Typography variant="body2" color="text.secondary">
                        {center.currentLoad} t
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>{center.dailyProcessed} t</TableCell>
                <TableCell>
                  <Chip
                    label={`${center.efficiency}%`}
                    color={getEfficiencyColor(center.efficiency)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{center.lastUpdate}</TableCell>
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

export default TriCenters; 