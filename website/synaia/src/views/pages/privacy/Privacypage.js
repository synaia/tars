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
    title: 'Privacy',
  },
];

const Privacypage = () => {
  return (
    <PageContainer title="Privacy Policy | Synaia" description="Synaia privacy page">
      <LpHeader />
      <Container maxWidth="lg">
        <Grid container justifyContent="space-between" spacing={3}>
          <Grid item xs={12} sm={12} lg={12}>
            <Breadcrumb title="Privacy Policy" items={BCrumb}>
              <Box>
                <img src={breadcrumbImg} alt={breadcrumbImg} width={'165px'} />
              </Box>
            </Breadcrumb>

            <Container maxWidth="lg">
              <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
                <h2>Introduction</h2>
                <p>
                  At Synaia Automation & AI Consulting OÜ, we are committed to protecting your privacy and ensuring the security of your personal information.
                  This Privacy Policy outlines how we collect, use, disclose, and safeguard your data when you visit our website and
                  use our services.
                </p>

                <h2>Information We Collect</h2>
                <p>We collect various types of information to provide and improve our services, including:</p>
                <ul>
                  <li>
                    <strong>Personal Information:</strong> This may include your name, email address, phone number, and other contact details.
                  </li>
                  <li>
                    <strong>Usage Data:</strong> Information about how you interact with our website, such as your IP address, browser type,
                    and pages visited.
                  </li>
                  <li>
                    <strong>Cookies and Tracking Technologies:</strong> We use cookies and similar technologies to track activity on our
                    website and store certain information.
                  </li>
                </ul>

                <h2>How We Use Your Information</h2>
                <p>We use the information we collect for various purposes, including:</p>
                <ul>
                  <li>
                    <strong>To Provide and Maintain Our Services:</strong> Ensuring our services function properly and are accessible.
                  </li>
                  <li>
                    <strong>To Improve Our Services:</strong> Analyzing how you use our services to enhance functionality and user experience.
                  </li>
                  <li>
                    <strong>To Communicate With You:</strong> Sending updates, marketing communications, and responding to your inquiries.
                  </li>
                  <li>
                    <strong>To Ensure Security:</strong> Monitoring and analyzing usage to detect and prevent fraudulent activities.
                  </li>
                </ul>

                <h2>Information Sharing and Disclosure</h2>
                <p>We do not sell your personal information. We may share your information with:</p>
                <ul>
                  <li>
                    <strong>Service Providers:</strong> Third-party companies that assist us in providing our services, such as hosting
                    providers and analytics services.
                  </li>
                  <li>
                    <strong>Legal Requirements:</strong> If required by law or in response to valid requests by public authorities.
                  </li>
                </ul>

                <h2>Data Security</h2>
                <p>
                  We implement robust security measures to protect your personal information from unauthorized access, alteration, or
                  disclosure. However, no method of transmission over the internet or electronic storage is completely secure, and we cannot
                  guarantee absolute security.
                </p>

                <h2>Your Privacy Rights</h2>
                <p>
                  Depending on your location, you may have certain rights regarding your personal information, such as the right to access,
                  correct, or delete your data. To exercise these rights, please contact us using the details provided below.
                </p>

                <h2>Changes to This Privacy Policy</h2>
                <p>
                  We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page
                  and updating the "Effective Date" at the top.
                </p>

                <h2>Contact Us</h2>
                <p>If you have any questions about this Privacy Policy or our data practices, please contact us.</p>
                
                <p>
                  Thank you for trusting Synaia Automation & AI Consulting OÜ with your personal information. We are committed to protecting your privacy and ensuring
                  your data is secure.
                </p>
              </div>
            </Container>

          </Grid>
        </Grid>
        <hr style={{ border: 0, height: '1px', background: 'linear-gradient(to right, #0000008f, #84fab0, #8fd3f4, #0000008f)', margin: '20px 0', opacity: 0.8 }} />
      </Container>
      <Footer2 />
    </PageContainer>
  );
};

export default Privacypage;
