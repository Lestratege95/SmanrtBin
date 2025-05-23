import React, { useState, useMemo } from 'react';
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
  Card,
  CardContent,
  Tabs,
  Tab,
  Badge,
} from '@mui/material';
import Grid from '@mui/material/Grid';

import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  CheckCircle as ResolvedIcon,
  NotificationsActive as ActiveIcon
} from '@mui/icons-material';


interface Alert {
  id: number;
  binId: string;
  binName: string;
  zone: string;
  type: 'full' | 'maintenance' | 'error' | 'other';
  priority: 'high' | 'medium' | 'low';
  status: 'active' | 'resolved' | 'pending';
  message: string;
  createdAt: string;
  resolvedAt?: string;
}

const mockAlerts: Alert[] = [
  {
    id: 1,
    binId: 'BIN-001',
    binName: 'Poubelle-001',
    zone: 'Zone A',
    type: 'full',
    priority: 'high',
    status: 'active',
    message: 'Poubelle pleine à 95%',
    createdAt: '2024-03-20 08:30'
  },
  {
    id: 2,
    binId: 'BIN-002',
    binName: 'Poubelle-002',
    zone: 'Zone B',
    type: 'maintenance',
    priority: 'medium',
    status: 'pending',
    message: 'Maintenance requise - Capteur défectueux',
    createdAt: '2024-03-20 09:15'
  },
  {
    id: 3,
    binId: 'BIN-003',
    binName: 'Poubelle-003',
    zone: 'Zone C',
    type: 'error',
    priority: 'high',
    status: 'resolved',
    message: 'Erreur de communication',
    createdAt: '2024-03-20 07:45',
    resolvedAt: '2024-03-20 08:15'
  }
];

const getPriorityColor = (priority: Alert['priority']) => {
  switch (priority) {
    case 'high':
      return 'error';
    case 'medium':
      return 'warning';
    case 'low':
      return 'info';
    default:
      return 'default';
  }
};

const getTypeIcon = (type: Alert['type']) => {
  switch (type) {
    case 'full':
      return <ErrorIcon />;
    case 'maintenance':
      return <WarningIcon />;
    case 'error':
      return <ErrorIcon />;
    case 'other':
      return <InfoIcon />;
    default:
      return <InfoIcon />;
  }
};

const getStatusColor = (status: Alert['status']) => {
  switch (status) {
    case 'active':
      return 'error';
    case 'pending':
      return 'warning';
    case 'resolved':
      return 'success';
    default:
      return 'default';
  }
};

const StatCard = ({ title, value, color }: { title: string; value: number; color: string }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Typography color="text.secondary" gutterBottom>
        {title}
      </Typography>
      <Typography variant="h4" color={color}>
        {value}
      </Typography>
    </CardContent>
  </Card>
);

const AlertStats = ({ alerts }: { alerts: Alert[] }) => {
  const counts = useMemo(() => 
    alerts.reduce((acc, alert) => {
      if (alert.status === 'active') acc.active++;
      if (alert.status === 'pending') acc.pending++;
      if (alert.status === 'resolved') acc.resolved++;
      if (alert.priority === 'high') acc.highPriority++;
      return acc;
    }, { active: 0, pending: 0, resolved: 0, highPriority: 0 }),
    [alerts]
  );

  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' }, gap: 3, mb: 3 }}>
      <Box>
        <StatCard
          title="Alertes actives"
          value={counts.active}
          color="error.main"
        />
      </Box>
      <Box>
        <StatCard
          title="En attente"
          value={counts.pending}
          color="warning.main"
        />
      </Box>
      <Box>
        <StatCard
          title="Résolues"
          value={counts.resolved}
          color="success.main"
        />
      </Box>
      <Box>
        <StatCard
          title="Priorité haute"
          value={counts.highPriority}
          color="error.main"
        />
      </Box>
    </Box>
  );
};

const Alerts = () => {
  const [alerts, setAlerts] = useState<Alert[]>(mockAlerts);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gestion des alertes
        </Typography>
        <Box>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ mr: 1 }}
          >
            Nouvelle alerte
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
          >
            Actualiser
          </Button>
        </Box>
      </Box>

      <AlertStats alerts={alerts} />

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab 
            label={
              <Badge badgeContent={alerts.filter(a => a.status === 'active').length} color="error">
                Actives
              </Badge>
            } 
          />
          <Tab 
            label={
              <Badge badgeContent={alerts.filter(a => a.status === 'pending').length} color="warning">
                En attente
              </Badge>
            } 
          />
          <Tab label="Résolues" />
          <Tab label="Toutes" />
        </Tabs>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Poubelle</TableCell>
              <TableCell>Zone</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Priorité</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Message</TableCell>
              <TableCell>Créée le</TableCell>
              <TableCell>Résolue le</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {alerts.map((alert) => (
              <TableRow key={alert.id}>
                <TableCell>{alert.id}</TableCell>
                <TableCell>{alert.binName}</TableCell>
                <TableCell>{alert.zone}</TableCell>
                <TableCell>
                  <Chip
                    icon={getTypeIcon(alert.type)}
                    label={alert.type}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={alert.priority}
                    color={getPriorityColor(alert.priority)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={alert.status}
                    color={getStatusColor(alert.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{alert.message}</TableCell>
                <TableCell>{alert.createdAt}</TableCell>
                <TableCell>{alert.resolvedAt || '-'}</TableCell>
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

export default Alerts; 