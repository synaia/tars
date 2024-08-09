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
import Footer2 from '../../../components/landingpage/footer/Footer2';
import Frameworks from '../../../components/landingpage/frameworks/Frameworks';
import LpHeader from '../../../components/landingpage/header/Header';
import Testimonial from '../../../components/landingpage/testimonial/Testimonial';
import Breadcrumb from 'src/layouts/full/shared/breadcrumb/Breadcrumb';
import breadcrumbImg from 'src/assets/images/breadcrumb/ChatBc.png';
import Service1 from 'src/components/apps/services/Service1';

import logoIcon from 'src/assets/images/logos/logoIcon.svg';
import workingVideo from 'src/assets/videos/working.mp4';
import MisionVision from '../../../components/landingpage/features/MisionVision';

import {
  FbContactForm,
  FbContact2Form,
} from '../../../components/forms/form-layouts/index';
import { borderRadius } from '@mui/system';

const BCrumb = [
  {
    to: '/',
    title: 'Home',
  },
  {
    to: '/services',
    title: 'Services',
  },
  {
    title: 'Software Development',
  },
];

const Servicespage1 = () => {
  return (
    <PageContainer title="Software Development | Synaia" description="Synaia services page">
      <LpHeader />
      <Container maxWidth="lg">
        <Grid container justifyContent="space-between" spacing={3}>
          <Grid item xs={12} sm={12} lg={12}>
            <Breadcrumb title="Software Development" items={BCrumb}>
              <Box>
                <img src={breadcrumbImg} alt={breadcrumbImg} width={'165px'} />
              </Box>
            </Breadcrumb>
          </Grid>
        </Grid>
        <Service1 />
        </Container>
        <hr style={{ border: 0, height: '1px', background: 'linear-gradient(to right, #0000008f, #84fab0, #8fd3f4, #0000008f)', margin: '20px 0', opacity: 0.8 }} />
      <Footer2 />
    </PageContainer>
  );
};

export default Servicespage1;
