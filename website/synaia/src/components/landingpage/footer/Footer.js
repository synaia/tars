import React from 'react';
import { Grid, Link, Typography, Container } from '@mui/material';
import {
  FbContact2Form,
} from '../../../components/forms/form-layouts/index';

import logoIcon from 'src/assets/images/logos/logoIcon.svg';

const Footer = () => {
  return (
    <Container maxWidth="lg">
      <Grid container spacing={3} justifyContent="center" mt={4}>
        <Grid item xs={12} sm={5} lg={4} textAlign="center">
          <img src={logoIcon} alt="icon" />
          <Typography fontSize="16" color="textSecondary" mt={1} mb={4}>
            Copyright &copy; 2024 Synaia Automation & AI Consulting OÜ | All rights reserved.
          </Typography>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Footer;
