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
    title: 'Contact',
  },
];

const Aboutpage = () => {
  return (
    <PageContainer title="About | Synaia" description="Synaia about us page">
      <LpHeader />
      <Container maxWidth="lg">
        <Grid container justifyContent="space-between" spacing={3}>
          <Grid item xs={12} sm={12} lg={12}>
            <Breadcrumb title="About Us" subtitle="At Synaia, we harness the power of AI and deep learning to revolutionize businesses. Discover how our innovative technological solutions can drive your success and exceed your expectations.">
              <Box>
                <img src={breadcrumbImg} alt={breadcrumbImg} width={'165px'} />
              </Box>
            </Breadcrumb>

            <Container maxWidth="lg">
              <form>
                <Grid container spacing={3} mb={3} textAlign="left">
                  <Grid item lg={6} md={12} sm={12}>
                    <p>Founded in early 2024 in Europe, Synaia is a multi-country company leading the way in AI and deep learning solutions. We specialize in transforming businesses through advanced technologies that enhance efficiency, improve decision-making, and open new avenues for growth. Our team of skilled professionals is dedicated to providing tailored solutions that cater to the unique needs of each client, delivering exceptional results every time.</p>
                    <p>At Synaia, we are driven by our commitment to excellence and our desire to push the limits of innovation. With extensive experience and expertise, we develop intelligent systems that address complex challenges and offer a competitive advantage. Discover how Synaia can revolutionize your business and help you achieve your objectives through the power of cutting-edge technology.</p>
                  </Grid>
                  <Grid item lg={6} md={12} sm={12} textAlign="left" paddingLeft={5}>
                    <Grid item lg={12} md={12} sm={12} textAlign="center">
                      <video width="100%" height="auto" loop autoPlay muted>
                        <source src={workingVideo} type="video/mp4" />
                        Your browser does not support the video tag.
                      </video>
                    </Grid>
                    <div>

                    </div>
                  </Grid>
                </Grid>
              </form>
            </Container>

          </Grid>
        </Grid>

        <MisionVision />
        <hr style={{ border: 0, height: '1px', background: 'linear-gradient(to right, #0000008f, #84fab0, #8fd3f4, #0000008f)', margin: '20px 0', opacity: 0.8 }} />
      </Container>
      <Footer2 />
    </PageContainer>
  );
};

export default Aboutpage;
