import React from 'react';
import { Box, Container, Button, styled, Typography, Grid, Avatar,  Chip } from '@mui/material';
import './demo-slider.css';
import DemoTitle from './DemoTitle';

import {
  IconArchive,
} from '@tabler/icons';

import AnimationFadeIn from '../animation/Animation';

// images
import codingService from 'src/assets/images/landingpage/services/programming.png';
import aiService from 'src/assets/images/landingpage/services/ai.png';
import dsService from 'src/assets/images/landingpage/services/data-science.png';
import wsService from 'src/assets/images/landingpage/services/whatsapp.png';

const StyledBox = styled(Box)(() => ({
  overflow: 'auto',
  position: 'relative',
  '.MuiButton-root': {
    display: 'none',
  },
  '&:hover': {
    '.MuiButton-root': {
      display: 'block',
      transform: 'translate(-50%,-50%)',
      position: 'absolute',
      left: '50%',
      right: '50%',
      top: '50%',
      minWidth: '100px',
      zIndex: '9',
    },
    '&:before': {
      content: '""',
      position: 'absolute',
      top: '0',
      left: ' 0',
      width: '100%',
      height: '100%',
      zIndex: '8',
      backgroundColor: 'rgba(55,114,255,.2)',
    },
  },
}));

const demos = [
  {
    link: 'https://www.synaia.io',
    img: codingService,
    title: 'Software Development',
  },
  {
    link: 'https://www.synaia.io',
    img: aiService,
    title: 'AI Automations',
  },
  {
    link: 'https://www.synaia.io',
    img: dsService,
    title: 'Data Science',
  },
  {
    link: 'https://www.synaia.io',
    img: wsService,
    title: 'What\sApp Workflows',
  },
];


const DemoSlider = () => {
  return (
    <Box
      mt="50px"
      pb="140px"
      className="customProperties"
      overflow="hidden"
      sx={{
        pt: {
          sm: '60px',
          lg: '0',
        },
      }}
    >
      <Container maxWidth="lg">
        {/* Title */}
        <DemoTitle />

        {/* slider */}
        <Box mt={9}>
          <Grid container spacing={3} justifyContent="center">
            {demos.map((demo, index) => (
              <Grid item xs={12} lg={3} key={index}>
                <Box>
                  {/* <Link href={demo.link}> */}
                  <StyledBox>
                    <Avatar
                      src={demo.img}
                      sx={{
                        borderRadius: '8px',
                        width: '100%',
                        height: '90%',
                        paddingLeft: '15%',
                        paddingRight: '15%',
                        paddingTop: '5%',
                        paddingBottom: '5%'
                      }}
                    />
                    <Button
                      variant="contained"
                      color="primary"
                      size="small"
                      href={demo.link}
                      target="_blank"
                      sx={{
                        textAlign: 'center',
                        color: '#000',
                        border: '1px solid #000'
                      }}
                    >
                      More Info
                    </Button>
                  </StyledBox>
                  {/* </Link> */}
                  <Typography
                    variant="body1"
                    color="textPrimary"
                    textAlign="center"
                    fontWeight={500}
                    mt={2}
                  >
                    {demo.title}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Box>
  );
};

export default DemoSlider;
