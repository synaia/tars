import React from 'react';
import { Grid, Link, Typography, Container, Box } from '@mui/material';
import {
  FbContact2Form,
} from '../../../components/forms/form-layouts/index';

import logoIcon from 'src/assets/images/logos/logoIcon.svg';

const Footer = () => {
  return (
    // <Container maxWidth="lg">
    //   <Grid container spacing={3} justifyContent="left" mt={4}>

    //     <FbContact2Form />
    //     <Grid item xs={12} sm={5} lg={4} textAlign="center">
    //       <Typography fontSize="16" color="textSecondary" mt={1} mb={4}>
    //       Copyright &copy; 2024 Synaia Automation & AI Consulting OÜ | All rights reserved.
    //       </Typography>
    //     </Grid>
    //   </Grid>
    //   <Grid item lg={6} md={12} sm={12}>
    //     <img src={logoIcon} alt="icon" width={'100px'} />
    //   </Grid>

    // </Container>
    <Container maxWidth="lg">
      <form>
        <Grid container spacing={3} mb={3} textAlign="left">
          <Grid item lg={6} md={12} sm={12}>
            <FbContact2Form />
          </Grid>
          <Grid item lg={6} md={12} sm={12} textAlign="left" paddingLeft={5}>
            <Grid item lg={12} md={12} sm={12} textAlign="center">
              <img src={logoIcon} alt="icon" width={'20%'} />
            </Grid>
            <div>
              <Typography fontSize="16" color="textSecondary" mt={1} mb={4} textAlign={'justify'} ml={2} mr={2}>
              At Synaia, we pride ourselves on delivering exceptional technological solutions that push the boundaries of innovation. We specialize in implementing cutting-edge AI and deep learning technologies to transform businesses and drive success. Our team of experts is dedicated to creating intelligent systems that not only meet but exceed our clients’ expectations. 
              </Typography>
              <Box display="flex" justifyContent="Left" mb={4}>
                <Link href="/privacy" color="inherit" underline="none" mx={2}>
                  Privacy
                </Link>
                <span>|</span>
                <Link href="/terms-and-conditions" color="inherit" underline="none" mx={2}>
                  Terms and conditions
                </Link>
              </Box>
            </div>
          </Grid>
        </Grid>
        <Grid item lg={12} md={12} sm={12} textAlign="center">
          <Typography fontSize="16" color="textSecondary" mt={1} mb={4} >
            Copyright &copy; 2024 Synaia Automation & AI Consulting OÜ | All rights reserved.
          </Typography>
        </Grid>
      </form>
    </Container>
  );
};

export default Footer;
