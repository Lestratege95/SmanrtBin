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
  Chip
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

interface Bin {
  id: number;
  name: string;
  location: string;
  status: 'active' | 'maintenance' | 'full';
  lastCollection: string;
}

const mockBins: Bin[] = [
  {
    id: 1,
    name: 'Poubelle-001',
    location: 'Zone A',
    status: 'active',
    lastCollection: '2024-03-20'
  },
  {
    id: 2,
    name: 'Poubelle-002',
    location: 'Zone B',
    status: 'full',
    lastCollection: '2024-03-19'
  },
  {
    id: 3,
    name: 'Poubelle-003',
    location: 'Zone C',
    status: 'maintenance',
    lastCollection: '2024-03-18'
  }
];

const getStatusColor = (status: Bin['status']) => {
  switch (status) {
    case 'active':
      return 'success';
    case 'maintenance':
      return 'warning';
    case 'full':
      return 'error';
    default:
      return 'default';
  }
};

const Bins = () => {
  const [bins, setBins] = useState<Bin[]>(mockBins);

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gestion des poubelles
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

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nom</TableCell>
              <TableCell>Emplacement</TableCell>
              <TableCell>Statut</TableCell>
              <TableCell>Dernière collecte</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {bins.map((bin) => (
              <TableRow key={bin.id}>
                <TableCell>{bin.id}</TableCell>
                <TableCell>{bin.name}</TableCell>
                <TableCell>{bin.location}</TableCell>
                <TableCell>
                  <Chip
                    label={bin.status}
                    color={getStatusColor(bin.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{bin.lastCollection}</TableCell>
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

export default Bins; 