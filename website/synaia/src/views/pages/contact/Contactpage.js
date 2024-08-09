import React from 'react';
import PageContainer from 'src/components/container/PageContainer';
import { Grid, Typography, Box, Button, styled, Container, Stack } from '@mui/material';
import { NavLink } from 'react-router-dom';
// components
import Banner from '../../../components/landingpage/banner/Banner';
import C2a from '../../../components/landingpage/c2a/C2a';
import C2a2 from '../../../components/landingpage/c2a/C2a2';
import DemoSlider from '../../../components/landingpage/demo-slider/DemoSlider';
import Features from '../../../components/landingpage/features/Features';
import Footer from '../../../components/landingpage/footer/Footer';
import Frameworks from '../../../components/landingpage/frameworks/Frameworks';
import LpHeader from '../../../components/landingpage/header/Header';
import Testimonial from '../../../components/landingpage/testimonial/Testimonial';
import Breadcrumb from 'src/layouts/full/shared/breadcrumb/Breadcrumb';
import breadcrumbImg from 'src/assets/images/breadcrumb/emailSv.png';
import {
  FbContactForm,
  FbContact2Form,
} from '../../../components/forms/form-layouts/index';

const BCrumb = [
  {
    to: '/',
    title: 'Home',
  },
  {
    title: 'Contact',
  },
];

const Contactpage = () => {
  return (
    <PageContainer title="Contact | Synaia" description="Synaia contact page">
      <LpHeader />
      <Container maxWidth="lg">
        <Grid container justifyContent="space-between" spacing={3}>
          <Grid item xs={12} sm={12} lg={12}>
          <Breadcrumb title="Contact Us" subtitle="Reach Out Today! Your questions are important. For more information, please use the suggested contact methods to get the assistance you need.">
            <Box>
              <img src={breadcrumbImg} alt={breadcrumbImg} width={'165px'} />
            </Box>
          </Breadcrumb>
          <FbContact2Form />
          <FbContactForm />
          </Grid>
        </Grid>
      </Container>
      <Footer />
    </PageContainer>
  );
};

export default Contactpage;
