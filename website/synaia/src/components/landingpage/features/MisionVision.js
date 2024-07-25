import React from 'react';
import FeaturesTitle from './FeaturesTitle';
import { Typography, Grid, Container, Box } from '@mui/material';
import {
  IconAdjustments,
  IconArchive,
  IconArrowsShuffle,
  IconBook,
  IconBuildingCarousel,
  IconCalendar,
  IconChartPie,
  IconDatabase,
  IconDiamond,
  IconLanguageKatakana,
  IconLayersIntersect,
  IconMessages,
  IconRefresh,
  IconRobot,
  IconShieldLock,
  IconMoodCrazyHappy,
  IconMoodSmile,
  IconTag,
  IconAd2,
  IconReportMedical,
  IconWand,
} from '@tabler/icons';
import AnimationFadeIn from '../animation/Animation';

const featuresData = [
  {
    icon: <IconRobot width={80} height={80} strokeWidth={1.5} />,
    title: 'Mission',
    subtext: 'To help businesses enhance efficiency through the implementation of advanced technological solutions.',
  },
  {
    icon: <IconMoodSmile width={80} height={80} strokeWidth={1.5} />,
    title: 'Vision',
    subtext: 'To create greater results for our clients and partners, driving success and innovation with the Artificial Intelligence.',
  },
  {
    icon: <IconAdjustments width={80} height={80} strokeWidth={1.5} />,
    title: 'Values',
    subtext: (
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        <li><b>Innovation:</b> We continuously push the boundaries of technology to provide cutting-edge solutions.</li>
        <li><b>Integrity:</b> We uphold the highest standards of honesty and transparency in all our actions.</li>
        <li><b>Customer Focus:</b> We prioritize our clients’ needs and strive to exceed their expectations.</li>
      </ul>
    ),
  }
];

const MisionVision = () => {
  return (
    <Box py={4}>
      <Container maxWidth="lg" >
        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} sm={10} lg={6}>
            <Typography fontSize="16" textTransform="uppercase" color="primary.main" fontWeight={500} textAlign="center" mb={1}>Know more</Typography>
          </Grid>
        </Grid>

        <Box mt={4}>
          <Grid container spacing={6}>
            {featuresData.map((feature, index) => (
              <Grid item xs={12} sm={4} lg={4} textAlign="center" key={index}>
                <AnimationFadeIn>
                  <Box color="primary.main">{feature.icon}</Box>
                  <Typography variant="h5" mt={3}>
                    {feature.title}
                  </Typography>
                  <Typography variant="subtitle1" color="textSecondary" mt={1} mb={3}>
                    {feature.subtext}
                  </Typography>
                </AnimationFadeIn>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Box>
  );
};

export default MisionVision;
