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
    title: 'Terms and Conditions',
  },
];

const Termspage = () => {
  return (
    <PageContainer title="Terms and Conditions | Synaia" description="Synaia Terms and Conditions page">
      <LpHeader />
      <Container maxWidth="lg">
        <Grid container justifyContent="space-between" spacing={3}>
          <Grid item xs={12} sm={12} lg={12}>
            <Breadcrumb title="Terms and Conditions" items={BCrumb}>
              <Box>
                <img src={breadcrumbImg} alt={breadcrumbImg} width={'165px'} />
              </Box>
            </Breadcrumb>

            <Container maxWidth="lg">
              <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
                <h2>Introduction</h2>
                <p>
                  Welcome to Synaia Automation & AI Consulting OÜ. These terms and conditions outline the rules and regulations for the use of our website and services.
                  By accessing this website, we assume you accept these terms and conditions. Do not continue to use Synaia Automation & AI Consulting OÜ if you do not
                  agree to all the terms and conditions stated on this page.
                </p>

                <h2>License</h2>
                <p>
                  Unless otherwise stated, Synaia Automation & AI Consulting OÜ and/or its licensors own the intellectual property rights for all material on Synaia Automation & AI Consulting OÜ.
                  All intellectual property rights are reserved. You may access this from Synaia Automation & AI Consulting OÜ for your own personal use subjected to
                  restrictions set in these terms and conditions.
                </p>
                <p>You must not:</p>
                <ul>
                  <li>Republish material from Synaia Automation & AI Consulting OÜ</li>
                  <li>Sell, rent, or sub-license material from Synaia Automation & AI Consulting OÜ</li>
                  <li>Reproduce, duplicate, or copy material from Synaia Automation & AI Consulting OÜ</li>
                  <li>Redistribute content from Synaia Automation & AI Consulting OÜ</li>
                </ul>

                <h2>Acceptable Use</h2>
                <p>
                  You agree to use our website only for lawful purposes and in a way that does not infringe the rights of, restrict, or inhibit
                  anyone else's use and enjoyment of the website. Prohibited behavior includes harassing or causing distress or inconvenience
                  to any other user, transmitting obscene or offensive content, or disrupting the normal flow of dialogue within our website.
                </p>

                <h2>User Accounts</h2>
                <p>
                  If you create an account on our website, you are responsible for maintaining the security of your account, and you are fully
                  responsible for all activities that occur under the account and any other actions taken in connection with it. You must
                  immediately notify us of any unauthorized uses of your account or any other breaches of security.
                </p>

                <h2>Limitation of Liability</h2>
                <p>
                  Synaia Automation & AI Consulting OÜ shall not be liable for any direct, indirect, incidental, special, or consequential damages resulting from the use
                  or the inability to use our website or services. This includes, but is not limited to, damages for errors, omissions,
                  interruptions, defects, delays in operation or transmission, computer virus, or line failure.
                </p>

                <h2>Indemnification</h2>
                <p>
                  You agree to indemnify and hold harmless Synaia Automation & AI Consulting OÜ, its contractors, and its licensors, and their respective directors,
                  officers, employees, and agents from and against any and all claims and expenses, including attorneys’ fees, arising out of
                  your use of our website, including but not limited to your violation of this Agreement.
                </p>

                <h2>Governing Law</h2>
                <p>
                  These terms and conditions are governed by and construed in accordance with the laws of Europa, and you
                  irrevocably submit to the exclusive jurisdiction of the courts in that location.
                </p>

                <h2>Changes to These Terms</h2>
                <p>
                  We may update our Terms and Conditions from time to time. We will notify you of any changes by posting the new Terms and
                  Conditions on this page and updating the "Effective Date" at the top.
                </p>

                <h2>Contact Us</h2>
                <p>If you have any questions about these Terms and Conditions, please contact us.</p>

                <p>Thank you for visiting Synaia Automation & AI Consulting OÜ. We hope you have a productive and enjoyable experience.</p>
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

export default Termspage;
